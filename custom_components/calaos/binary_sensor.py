from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import Platform

from pycalaos.item import io

from .entity import CalaosEntity, setup_entities


class InPlageHoraire(CalaosEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.RUNNING

    @property
    def icon(self) -> str:
        return "mdi:clock-check-outline" if self.item.state else "mdi:clock-outline"

    @property
    def is_on(self) -> bool:
        return self.item.state


mapping = {
    io.InPlageHoraire: InPlageHoraire,
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities(
        setup_entities(hass, config_entry.entry_id, mapping, Platform.BINARY_SENSOR)
    )
