import logging

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .entity import CalaosEntity, setup_entities

from pycalaos.item import io

_LOGGER = logging.getLogger(__name__)


def is_a_switch(item: io.OutputLight) -> bool:
    return is_a_regular_switch(item) or is_an_outlet(item)


def is_a_regular_switch(item: io.OutputLight) -> bool:
    return item.name.startswith("SW ")


def is_an_outlet(item: io.OutputLight) -> bool:
    return item.name.startswith("OU ")


class InternalBool(CalaosEntity, SwitchEntity):
    _attr_icon = "mdi:toggle-switch-outline"

    @property
    def is_on(self) -> bool:
        return self.item.state

    def turn_on(self, **kwargs) -> None:
        self.item.true()
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        self.item.false()
        self.schedule_update_ha_state()


class OutputLightAsSwitch(CalaosEntity, SwitchEntity):
    _remove_prefix = "SW "

    @property
    def is_on(self) -> bool:
        return self.item.state

    def turn_on(self, **kwargs) -> None:
        self.item.true()
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        self.item.false()
        self.schedule_update_ha_state()


class OutputLightAsOutlet(CalaosEntity, SwitchEntity):
    _attr_device_class: SwitchDeviceClass.OUTLET
    _remove_prefix = "OU "

    @property
    def is_on(self) -> bool:
        return self.item.state

    def turn_on(self, **kwargs) -> None:
        self.item.true()
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        self.item.false()
        self.schedule_update_ha_state()


class Scenario(CalaosEntity, SwitchEntity):
    _attr_icon = "mdi:motion-play-outline"

    @property
    def is_on(self) -> bool:
        return self.item.state

    def turn_on(self, **kwargs) -> None:
        self.item.true()
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        self.item.false()
        self.schedule_update_ha_state()


mapping = {
    io.InternalBool: InternalBool,
    io.Scenario: Scenario,
}


def setup_switch_entities(
    hass: HomeAssistant,
    entry_id: str,
) -> list[Entity]:
    coordinator = hass.data[DOMAIN][entry_id]
    entities = []
    for item in coordinator.client.items_by_type(io.OutputLight):
        if is_a_regular_switch(item):
            _LOGGER.debug("Creating entity for %s", item.name)
            entity = OutputLightAsSwitch(hass, entry_id, item, Platform.SWITCH)
            coordinator.register(item.id, entity)
            entities.append(entity)
        elif is_an_outlet(item):
            _LOGGER.debug("Creating entity for %s", item.name)
            entity = OutputLightAsOutlet(hass, entry_id, item, Platform.SWITCH)
            coordinator.register(item.id, entity)
            entities.append(entity)
    return entities


async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities(setup_switch_entities(hass, config_entry.entry_id))
    async_add_entities(
        setup_entities(hass, config_entry.entry_id, mapping, Platform.SWITCH)
    )
