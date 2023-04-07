from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity
from homeassistant.const import Platform

from .const import DOMAIN
from .entity import CalaosEntity


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    for item in coordinator.client.items_by_gui_type("light"):
        entity = Light(hass, config_entry.entry_id, item)
        coordinator.register(item.id, entity)
        entities.append(entity)
    for item in coordinator.client.items_by_gui_type("light_dimmer"):
        entity = LightDimmer(hass, config_entry.entry_id, item)
        coordinator.register(item.id, entity)
        entities.append(entity)
    async_add_entities(entities)
    return True


class Light(CalaosEntity, LightEntity):
    platform = Platform.LIGHT
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = [ColorMode.ONOFF]

    @property
    def is_on(self):
        return self.item.state

    def turn_on(self, **kwargs):
        self.item.turn_on()

    def turn_off(self, **kwargs):
        self.item.turn_off()


class LightDimmer(CalaosEntity, LightEntity):
    platform = Platform.LIGHT
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = [ColorMode.BRIGHTNESS]

    @property
    def brightness(self):
        return round(self.item.state / 100 * 255)

    @property
    def is_on(self):
        return self.item.state > 0

    def turn_on(self, **kwargs):
        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs[ATTR_BRIGHTNESS]
            self.item.set_brightness(max(1, round(brightness * 100 / 255)))
        else:
            self.item.turn_on()

    def turn_off(self, **kwargs):
        self.item.turn_off()
