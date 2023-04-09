import logging

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import CalaosEntity

_LOGGER = logging.getLogger(__name__)


def is_a_switch(item):
    return is_a_regular_switch(item) or is_an_outlet(item)


def is_a_regular_switch(item):
    return item.name.startswith("SW ")


def is_an_outlet(item):
    return item.name.startswith("OU ")


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    for item in coordinator.items_by_gui_type("light"):
        if is_a_regular_switch(item):
            _LOGGER.debug("Creating entity for %s", item.name)
            entity = Switch(hass, config_entry.entry_id, item)
            coordinator.register(item.id, entity)
            entities.append(entity)
        elif is_an_outlet(item):
            _LOGGER.debug("Creating entity for %s", item.name)
            entity = Outlet(hass, config_entry.entry_id, item)
            coordinator.register(item.id, entity)
            entities.append(entity)
    async_add_entities(entities)


class Switch(CalaosEntity, SwitchEntity):
    platform = Platform.SWITCH

    _remove_prefix = "SW "

    @property
    def is_on(self) -> bool:
        return self.item.state

    def turn_on(self, **kwargs) -> None:
        self.item.turn_on()

    def turn_off(self, **kwargs) -> None:
        self.item.turn_off()


class Outlet(CalaosEntity, SwitchEntity):
    platform = Platform.SWITCH
    _attr_device_class: SwitchDeviceClass.OUTLET

    _remove_prefix = "OU "

    @property
    def is_on(self) -> bool:
        return self.item.state

    def turn_on(self, **kwargs) -> None:
        self.item.turn_on()

    def turn_off(self, **kwargs) -> None:
        self.item.turn_off()
