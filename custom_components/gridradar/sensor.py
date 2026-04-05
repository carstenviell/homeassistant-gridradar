"""Sensor-Plattform für Gridradar."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_METRICS, DOMAIN, METRICS
from .coordinator import GridradarCoordinator

_LOGGER = logging.getLogger(__name__)

DEVICE_CLASS_MAP = {
    "frequency": SensorDeviceClass.FREQUENCY,
    "power": SensorDeviceClass.POWER,
}

STATE_CLASS_MAP = {
    "measurement": SensorStateClass.MEASUREMENT,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Sensoren aus einem Config-Entry aufsetzen."""
    coordinator: GridradarCoordinator = hass.data[DOMAIN][entry.entry_id]
    selected_metrics = entry.data[CONF_METRICS]

    entities = [
        GridradarSensor(coordinator, metric_id)
        for metric_id in selected_metrics
        if metric_id in METRICS
    ]

    async_add_entities(entities)


class GridradarSensor(CoordinatorEntity, SensorEntity):
    """Repräsentiert einen Gridradar-Sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GridradarCoordinator,
        metric_id: str,
    ) -> None:
        """Initialisierung."""
        super().__init__(coordinator)
        self._metric_id = metric_id
        metric_config = METRICS[metric_id]

        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{metric_id}"
        self._attr_name = metric_config["name"]
        self._attr_native_unit_of_measurement = metric_config["unit"]
        self._attr_icon = metric_config["icon"]

        device_class_str = metric_config.get("device_class")
        self._attr_device_class = DEVICE_CLASS_MAP.get(device_class_str) if device_class_str else None

        state_class_str = metric_config.get("state_class")
        self._attr_state_class = STATE_CLASS_MAP.get(state_class_str) if state_class_str else None

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Gridradar",
            manufacturer="Gridradar",
            model="Grid Monitoring API",
            configuration_url="https://service.gridradar.net",
        )

    @property
    def native_value(self) -> float | None:
        """Aktueller Messwert."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._metric_id)

    @property
    def available(self) -> bool:
        """Verfügbarkeit des Sensors."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and self.coordinator.data.get(self._metric_id) is not None
        )
