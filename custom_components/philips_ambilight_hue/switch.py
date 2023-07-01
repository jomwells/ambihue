"""Philips Ambilight+Hue switch"""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import PhilipsTVDataUpdateCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the configuration entry."""
    coordinator: PhilipsTVDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    async_add_entities([PhilipsTVAmbiHueSwitch(coordinator)])


class PhilipsTVAmbiHueSwitch(CoordinatorEntity, SwitchEntity):
    """A Philips TV Ambilight+Hue state switch."""

    coordinator: PhilipsTVDataUpdateCoordinator

    def __init__(
        self,
        coordinator: PhilipsTVDataUpdateCoordinator,
    ) -> None:
        """Initialize entity."""

        super().__init__(coordinator)

        self._attr_name = f"{coordinator.system['name']} Ambilight+Hue"
        self._attr_icon = "mdi:television-ambient-light"
        self._attr_unique_id = coordinator.unique_id
        self._attr_device_info = DeviceInfo(
            identifiers={
                (DOMAIN, self._attr_unique_id),
            },
            manufacturer="Philips",
            model=coordinator.system.get("model"),
            name=coordinator.system["name"],
            sw_version=coordinator.system.get("softwareversion"),
        )

    @property
    def available(self) -> bool:
        """Return true if entity is available."""
        if not super().available:
            return False
        if not self.coordinator.api.on:
            return False
        return self.coordinator.api.powerstate == "On"

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        return self.coordinator.huelampstate == "On"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.coordinator.setHueLampState("On")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.coordinator.setHueLampState("Off")
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.coordinator.huelampstate == "On"
        self.async_write_ha_state()
