import logging

from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity
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
    for item in coordinator.client.items_by_gui_type("light"):
        _LOGGER.debug("Creating entity for %s", item.name)
        entity = Light(hass, config_entry.entry_id, item)
        coordinator.register(item.id, entity)
        entities.append(entity)
    for item in coordinator.client.items_by_gui_type("light_dimmer"):
        _LOGGER.debug("Creating entity for %s", item.name)
        entity = LightDimmer(hass, config_entry.entry_id, item)
        coordinator.register(item.id, entity)
        entities.append(entity)
    async_add_entities(entities)


class Light(CalaosEntity, LightEntity):
    platform = Platform.LIGHT
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = [ColorMode.ONOFF]

    @property
    def is_on(self) -> bool:
        return self.item.state

    def turn_on(self, **kwargs) -> None:
        self.item.turn_on()

    def turn_off(self, **kwargs) -> None:
        self.item.turn_off()


class LightDimmer(CalaosEntity, LightEntity):
    platform = Platform.LIGHT
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = [ColorMode.BRIGHTNESS]

    @property
    def brightness(self) -> int:
        return round(self.item.state / 100 * 255)

    @property
    def is_on(self) -> bool:
        return self.item.state > 0

    def turn_on(self, **kwargs) -> None:
        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs[ATTR_BRIGHTNESS]
            self.item.set_brightness(max(1, round(brightness * 100 / 255)))
        else:
            self.item.turn_on()

    def turn_off(self, **kwargs) -> None:
        self.item.turn_off()
