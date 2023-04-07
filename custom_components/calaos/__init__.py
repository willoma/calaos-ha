"""Calaos integration for Home Assistant."""

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import CalaosCoordinator

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.LIGHT
]


async def async_setup_entry(hass, config_entry):
    coordinator = CalaosCoordinator(hass, config_entry)
    try:
        await coordinator.connect()
    except Exception as ex:
        raise ConfigEntryNotReady(f"Config Not Ready: {ex}")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    coordinator.declare_noentity_devices()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, coordinator.stop)
    config_entry.async_on_unload(coordinator.stop)

    config_entry.async_create_task(
        hass,
        hass.config_entries.async_forward_entry_setups(
            config_entry, PLATFORMS
        )
    )
    config_entry.async_create_background_task(
        hass,
        coordinator.pushing_poll(),
        "Calaos poller"
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
