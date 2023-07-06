from homeassistant.components.number import NumberEntity
from homeassistant.const import Platform

from .entity import CalaosEntity, setup_entities

from pycalaos.item import io

from .const import INTEGER_MIN, INTEGER_MAX


class InternalInt(CalaosEntity, NumberEntity):
    _attr_icon = "mdi:numeric"
    _attr_native_step = 1.0
    _attr_native_min_value = INTEGER_MIN
    _attr_native_max_value = INTEGER_MAX

    @property
    def native_value(self) -> float:
        return float(self.item.state)

    def set_native_value(self, value: float) -> None:
        self.item.set(int(value))
        self.schedule_update_ha_state()


mapping = {
    io.InternalInt: InternalInt,
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities(
        setup_entities(hass, config_entry.entry_id, mapping, Platform.NUMBER)
    )
