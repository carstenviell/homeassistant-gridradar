"""Gridradar-Integration für Home Assistant."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_API_TOKEN, CONF_METRICS, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import GridradarCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Integration über Config-Entry aufsetzen."""
    api_token = entry.data[CONF_API_TOKEN]
    selected_metrics = entry.data[CONF_METRICS]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    # Options überschreiben Data falls gesetzt
    if entry.options:
        selected_metrics = entry.options.get(CONF_METRICS, selected_metrics)
        scan_interval = entry.options.get(CONF_SCAN_INTERVAL, scan_interval)

    coordinator = GridradarCoordinator(
        hass,
        api_token=api_token,
        selected_metrics=selected_metrics,
        scan_interval=scan_interval,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Integration entladen."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Bei Änderung der Optionen die Integration neu laden."""
    await hass.config_entries.async_reload(entry.entry_id)
