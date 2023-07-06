import logging

from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from pycalaos.item import io

from .const import DOMAIN
from .entity import CalaosEntity, setup_entities
from .switch import is_a_switch

_LOGGER = logging.getLogger(__name__)


class OutputLight(CalaosEntity, LightEntity):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = [ColorMode.ONOFF]

    @property
    def is_on(self) -> bool:
        return self.item.state

    def turn_on(self, **kwargs) -> None:
        self.item.true()
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        self.item.false()
        self.schedule_update_ha_state()


class OutputLightDimmer(CalaosEntity, LightEntity):
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
            self.item.set(max(1, round(brightness * 100 / 255)))
        else:
            self.item.true()
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        self.item.false()
        self.schedule_update_ha_state()


mapping = {
    io.OutputLightDimmer: OutputLightDimmer,
}


def setup_light_entities(
    hass: HomeAssistant,
    entry_id: str,
) -> list[Entity]:
    coordinator = hass.data[DOMAIN][entry_id]
    entities = []
    for item in coordinator.client.items_by_type(io.OutputLight):
        if not is_a_switch(item):
            _LOGGER.debug("Creating entity for %s", item.name)
            entity = OutputLight(hass, entry_id, item, Platform.LIGHT)
            coordinator.register(item.id, entity)
            entities.append(entity)
    return entities


async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities(setup_light_entities(hass, config_entry.entry_id))
    async_add_entities(
        setup_entities(hass, config_entry.entry_id, mapping, Platform.LIGHT)
    )
