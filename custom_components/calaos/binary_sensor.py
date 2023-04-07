import logging

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import CalaosEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    for item in coordinator.client.items_by_gui_type("scenario"):
        _LOGGER.debug("Creating entity for %s", item.name)
        entity = Scenario(hass, config_entry.entry_id, item)
        coordinator.register(item.id, entity)
        entities.append(entity)
    for item in coordinator.client.items_by_gui_type("time_range"):
        _LOGGER.debug("Creating entity for %s", item.name)
        entity = TimeRange(hass, config_entry.entry_id, item)
        coordinator.register(item.id, entity)
        entities.append(entity)
    async_add_entities(entities)


class Scenario(CalaosEntity, BinarySensorEntity):
    platform = Platform.BINARY_SENSOR
    _attr_icon = "mdi:motion-play-outline"
    _attr_device_class = BinarySensorDeviceClass.RUNNING

    @property
    def is_on(self) -> bool:
        return self.item.state


class TimeRange(CalaosEntity, BinarySensorEntity):
    platform = Platform.BINARY_SENSOR
    _attr_device_class = BinarySensorDeviceClass.RUNNING

    @property
    def icon(self) -> str:
        return "mdi:clock-check-outline" if self.item.state else "mdi:clock-outline"

    @property
    def is_on(self) -> bool:
        return self.item.state
