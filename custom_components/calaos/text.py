from homeassistant.components.text import TextEntity
from homeassistant.const import Platform

from pycalaos.item import io

from .entity import CalaosEntity, setup_entities


class InternalString(CalaosEntity, TextEntity):
    _attr_icon = "mdi:alphabetical"

    @property
    def native_value(self) -> str:
        return self.item.state

    def set_value(self, value: str) -> None:
        self.item.set(value)
        self.schedule_update_ha_state()


mapping = {
    io.InternalString: InternalString,
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities(
        setup_entities(hass, config_entry.entry_id, mapping, Platform.TEXT)
    )
