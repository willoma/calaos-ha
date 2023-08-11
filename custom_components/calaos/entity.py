import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, Entity

from pycalaos.item.common import Item

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CalaosEntity:
    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_name = None

    _remove_prefix = ""

    def __init__(
        self, hass: HomeAssistant, entry_id: str, item: Item, platform
    ) -> None:
        self.entry_id = entry_id
        self.item = item
        self.hass = hass
        self._attr_unique_id = f"{DOMAIN}_{self.item.id}"
        self.entity_id = f"{platform}.{self.unique_id}"

    async def async_added_to_hass(self) -> None:
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry_id, self.item.id)},
            name=self.item.name.removeprefix(self._remove_prefix),
            manufacturer="Calaos",
            model="Calaos v3",
            suggested_area=self.item.room.name,
            via_device=(DOMAIN, self.entry_id),
        )


def setup_entities(
    hass: HomeAssistant,
    entry_id: str,
    mapping: dict[type, type],
    platform: str,
) -> list[Entity]:
    coordinator = hass.data[DOMAIN][entry_id]
    entities = []
    for libType, haEntity in mapping.items():
        for item in coordinator.client.items_by_type(libType):
            _LOGGER.debug("Declaring entity for %s", item.name)
            entity = haEntity(hass, entry_id, item, platform)
            coordinator.register(item.id, entity)
            entities.append(entity)
    return entities
