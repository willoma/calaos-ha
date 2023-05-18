from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from pycalaos.item import Item

from .const import DOMAIN


class CalaosEntity:
    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_name = None

    _remove_prefix = ""

    def __init__(self, hass: HomeAssistant, entry_id: str, item: Item) -> None:
        self.entry_id = entry_id
        self.item = item
        self.hass = hass
        self._attr_unique_id = f"{DOMAIN}_{self.item.id}"
        self.entity_id = f"{self.platform}.{self.unique_id}"

    async def async_added_to_hass(self) -> None:
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            config_entry_id=self.entry_id,
            identifiers={(DOMAIN, self.entry_id, self.item.id)},
            name=self.item.name.removeprefix(self._remove_prefix),
            manufacturer="Calaos",
            model="Calaos v3",
            suggested_area=self.item.room.name,
            via_device=(DOMAIN, self.entry_id),
        )
