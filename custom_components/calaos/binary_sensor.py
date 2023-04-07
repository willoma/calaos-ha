from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.const import Platform

from .const import DOMAIN
from .entity import CalaosEntity


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    for item in coordinator.client.items_by_gui_type("scenario"):
        entity = Scenario(hass, config_entry.entry_id, item)
        coordinator.register(item.id, entity)
        entities.append(entity)
    for item in coordinator.client.items_by_gui_type("time_range"):
        entity = TimeRange(hass, config_entry.entry_id, item)
        coordinator.register(item.id, entity)
        entities.append(entity)
    async_add_entities(entities)
    return True


class Scenario(CalaosEntity, BinarySensorEntity):
    platform = Platform.BINARY_SENSOR
    _attr_icon = "mdi:motion-play-outline"
    _attr_device_class = BinarySensorDeviceClass.RUNNING

    @property
    def is_on(self):
        return self.item.state


class TimeRange(CalaosEntity, BinarySensorEntity):
    platform = Platform.BINARY_SENSOR
    _attr_device_class = BinarySensorDeviceClass.RUNNING

    @property
    def icon(self):
        return "mdi:clock-check-outline" if self.item.state else "mdi:clock-outline"

    @property
    def is_on(self):
        return self.item.state
