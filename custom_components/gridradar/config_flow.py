"""Config-Flow für die Gridradar-Integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.selector as selector

from .const import (
    API_BASE_URL,
    CONF_API_TOKEN,
    CONF_METRICS,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    METRICS,
)

_LOGGER = logging.getLogger(__name__)

FREE_METRICS = [mid for mid, cfg in METRICS.items() if cfg["free_tier"]]


def _metric_selector() -> selector.SelectSelector:
    """Selector für die Metrik-Mehrfachauswahl."""
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[
                selector.SelectOptionDict(value=mid, label=cfg["name"])
                for mid, cfg in METRICS.items()
            ],
            multiple=True,
        )
    )


async def _validate_token(token: str) -> str | None:
    """API-Token prüfen. Gibt Fehlercode zurück oder None bei Erfolg."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{API_BASE_URL}/attrib",
                headers={"Authorization": f"Bearer {token}"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 401:
                    return "invalid_auth"
                if response.status not in (200, 204):
                    return "cannot_connect"
        except aiohttp.ClientError:
            return "cannot_connect"
    return None


class GridradarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config-Flow für Gridradar."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Schritt 1: API-Token und Metriken konfigurieren."""
        errors: dict[str, str] = {}

        if user_input is not None:
            token = user_input[CONF_API_TOKEN].strip()
            error = await _validate_token(token)

            if error:
                errors["base"] = error
            else:
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="Gridradar",
                    data={
                        CONF_API_TOKEN: token,
                        CONF_METRICS: user_input.get(CONF_METRICS, FREE_METRICS),
                        CONF_SCAN_INTERVAL: user_input.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_API_TOKEN): str,
                vol.Optional(CONF_METRICS, default=FREE_METRICS): _metric_selector(),
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(int, vol.Range(min=10, max=3600)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Options-Flow zurückgeben."""
        return GridradarOptionsFlow(config_entry)


class GridradarOptionsFlow(config_entries.OptionsFlow):
    """Options-Flow für Gridradar (Einstellungen nach der Ersteinrichtung)."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialisierung."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Einstellungen anzeigen und speichern."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_data = self.config_entry.data
        current_options = self.config_entry.options

        current_metrics = current_options.get(
            CONF_METRICS, current_data.get(CONF_METRICS, FREE_METRICS)
        )
        current_interval = current_options.get(
            CONF_SCAN_INTERVAL,
            current_data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )

        schema = vol.Schema(
            {
                vol.Optional(CONF_METRICS, default=current_metrics): _metric_selector(),
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=current_interval
                ): vol.All(int, vol.Range(min=10, max=3600)),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )
