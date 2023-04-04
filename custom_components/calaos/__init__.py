"""Calaos integration for Home Assistant."""

from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import CalaosCoordinator


async def async_setup(hass, config):
    return True


async def async_setup_entry(hass, config_entry):
    coordinator = CalaosCoordinator(hass, config_entry)
    try:
        await coordinator.connect()
    except Exception as ex:
        raise ConfigEntryNotReady(f"Config Not Ready: {ex}")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    coordinator.declare_noentity_devices()

    config_entry.async_create_task(
        hass,
        hass.config_entries.async_forward_entry_setups(
            config_entry, ["binary_sensor", "light"]
        )
    )
    config_entry.async_create_background_task(
        hass,
        coordinator.pushing_poll(),
        "Calaos poller"
    )
    return True
