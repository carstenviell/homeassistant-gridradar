"""DataUpdateCoordinator für Gridradar."""
from __future__ import annotations

import json
import logging
from datetime import timedelta

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, DOMAIN, METRICS

_LOGGER = logging.getLogger(__name__)


class GridradarCoordinator(DataUpdateCoordinator):
    """Koordinator für das Abrufen der Gridradar-Daten."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_token: str,
        selected_metrics: list[str],
        scan_interval: int,
    ) -> None:
        """Initialisierung."""
        self.api_token = api_token
        self.selected_metrics = selected_metrics

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        """Daten von der Gridradar-API abrufen."""
        results = {}

        async with aiohttp.ClientSession() as session:
            for metric_id in self.selected_metrics:
                metric_config = METRICS.get(metric_id)
                if not metric_config:
                    continue

                metric_key = metric_config["key"]
                url = f"{API_BASE_URL}/query"
                params = {
                    "metric": metric_key,
                    "aggr": "1m",
                    "func": "last",
                    "format": "json",
                    "ts": "rfc3339",
                }
                headers = {"Authorization": f"Bearer {self.api_token}"}

                try:
                    async with session.get(
                        url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        if response.status == 401:
                            raise ConfigEntryAuthFailed("Ungültiger API-Token")
                        if response.status == 403:
                            _LOGGER.warning(
                                "Keine Berechtigung für Metrik %s (evtl. nicht im Tarif enthalten)",
                                metric_key,
                            )
                            results[metric_id] = None
                            continue
                        if response.status != 200:
                            raise UpdateFailed(
                                f"Fehler beim Abrufen von {metric_key}: HTTP {response.status}"
                            )

                        raw = await response.text()
                        if not raw or not raw.strip():
                            _LOGGER.debug("Leere Antwort für Metrik %s", metric_key)
                            results[metric_id] = self.data.get(metric_id) if self.data else None
                            continue

                        try:
                            data = json.loads(raw)
                        except json.JSONDecodeError as err:
                            _LOGGER.warning("Ungültiges JSON für %s: %s", metric_key, err)
                            results[metric_id] = self.data.get(metric_id) if self.data else None
                            continue

                        value = self._extract_latest_value(data)
                        results[metric_id] = value

                except ConfigEntryAuthFailed:
                    raise
                except aiohttp.ClientError as err:
                    raise UpdateFailed(f"Verbindungsfehler: {err}") from err

        return results

    def _extract_latest_value(self, data: list) -> float | None:
        """Letzten Messwert aus der API-Antwort extrahieren."""
        if not data or not isinstance(data, list):
            return None

        series = data[0]
        datapoints = series.get("datapoints", [])

        if not datapoints:
            return None

        # Letzten Datenpunkt zurückgeben (Wert ist der erste Eintrag)
        last_point = datapoints[-1]
        if isinstance(last_point, (list, tuple)) and len(last_point) >= 1:
            return last_point[0]

        return None
