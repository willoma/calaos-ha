import logging
import re

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from pycalaos.item import io
from pycalaos.item.common import Item

from .entity import CalaosEntity, setup_entities

_LOGGER = logging.getLogger(__name__)

input_as_binary_sensor_re = re.compile("BIN(:[^ ]+)? ")

def is_a_binary_sensor(item: io.InputSwitch):
    return input_as_binary_sensor_re.match(item.name)


class InPlageHoraire(CalaosEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.RUNNING

    @property
    def icon(self) -> str:
        return "mdi:clock-check-outline" if self.item.state else "mdi:clock-outline"

    @property
    def is_on(self) -> bool:
        return self.item.state


def maybeBinarySensor(hass: HomeAssistant, entry_id: str, item: Item, platform):
    match = input_as_binary_sensor_re.match(item.name)
    if not match:
        return False
    return SwitchAsBinarySensor(hass, entry_id, match.group(1), item, platform)


class SwitchAsBinarySensor(CalaosEntity, BinarySensorEntity):
    def __init__(
        self,
        hass: HomeAssistant,
        entry_id: str,
        device_class: str,
        item: Item, platform
    ) -> None:
        _LOGGER.debug("Creating entity for %s", item.name)
        if device_class != "":
            self._attr_device_class = device_class[1:]
            self._remove_prefix = f"BIN:{device_class[1:]} "
        else:
            self._remove_prefix = "BIN "
        super(SwitchAsBinarySensor, self).__init__(hass, entry_id, item, platform)

mapping = {
    io.InPlageHoraire: InPlageHoraire,
    io.InputSwitch: maybeBinarySensor,
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities(
        setup_entities(hass, config_entry.entry_id, mapping, Platform.BINARY_SENSOR)
    )
