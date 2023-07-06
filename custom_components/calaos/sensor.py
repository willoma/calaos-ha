from homeassistant.components.sensor import SensorEntity
from homeassistant.const import Platform

from pycalaos.item import common, io

from .entity import CalaosEntity, setup_entities


class Default(CalaosEntity, SensorEntity):
    @property
    def native_value(self) -> str:
        return self.item.state


class InputAnalog(CalaosEntity, SensorEntity):
    _attr_icon = "mdi:numeric"

    @property
    def native_value(self) -> float:
        return self.item.state


class InputString(CalaosEntity, SensorEntity):
    _attr_icon = "mdi:alphabetical"

    @property
    def native_value(self) -> str:
        return self.item.state


class InputTemp(CalaosEntity, SensorEntity):
    _attr_icon = "mdi:thermometer"

    @property
    def native_value(self) -> str:
        return self.item.state


mapping = {
    common.Default: Default,
    io.InputAnalog: InputAnalog,
    io.InputString: InputString,
    io.InputTemp: InputTemp,
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities(
        setup_entities(hass, config_entry.entry_id, mapping, Platform.SENSOR)
    )
