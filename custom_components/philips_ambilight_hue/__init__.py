"""The Philips Ambilight+Hue integration."""
from __future__ import annotations

from typing import cast, Optional
import asyncio
from collections.abc import Mapping
from datetime import timedelta
import logging

from haphilipsjs import ConnectionFailure, PhilipsTV
from haphilipsjs.typing import SystemType

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_API_VERSION,
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import (
    HomeAssistant,
    callback,
)
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_SYSTEM, DOMAIN

PLATFORMS = [
    Platform.SWITCH,
]

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Philips TV from a config entry."""

    tvapi = PhilipsTV(
        entry.data[CONF_HOST],
        entry.data[CONF_API_VERSION],
        username=entry.data.get(CONF_USERNAME),
        password=entry.data.get(CONF_PASSWORD),
    )
    coordinator = PhilipsTVDataUpdateCoordinator(hass, tvapi, entry.options)

    await coordinator.async_refresh()
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_update_entry))

    return True


async def async_update_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class PhilipsTVDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Coordinator to update data."""

    def __init__(self, hass, api: PhilipsTV, options: Mapping) -> None:
        """Set up the coordinator."""
        self.api = api
        self.options = options
        
        self.huelampstate: Optional[str] = None

        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
            request_refresh_debouncer=Debouncer(
                hass, LOGGER, cooldown=2.0, immediate=False
            ),
        )

    @property
    def system(self) -> SystemType:
        """Return the system descriptor."""
        if self.api.system:
            return self.api.system
        return self.config_entry.data[CONF_SYSTEM]

    @property
    def unique_id(self) -> str:
        """Return the system descriptor."""
        entry: ConfigEntry = self.config_entry
        assert entry
        if entry.unique_id:
            return entry.unique_id
        assert entry.entry_id
        return entry.entry_id

    async def getHueLampState(self):
        r = await self.api.getReq("HueLamp/power")
        if r:
            self.huelampstate = cast(str, r["power"])
        else:
            self.huelampstate = None
        return r


    async def setHueLampState(self, state):
        data = {"power": state}
        if await self.api.postReq("HueLamp/power", data) is not None:
            self.huelampstate = state
            return True

    @callback
    async def _async_update_data(self):
        """Fetch the latest data from the source."""
        try:
            await self.getHueLampState()
            await self.api.update()
        except ConnectionFailure:
            pass
