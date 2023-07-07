from homeassistant.components.cover import (
    ATTR_POSITION,
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.const import Platform

from pycalaos.item import io

from .entity import CalaosEntity, setup_entities


class OutputShutterSmart(CalaosEntity, CoverEntity):
    _attr_device_class = CoverDeviceClass.SHUTTER
    _attr_supported_features = (
        CoverEntityFeature.OPEN
        | CoverEntityFeature.CLOSE
        | CoverEntityFeature.SET_POSITION
        | CoverEntityFeature.STOP
    )

    @property
    def current_cover_position(self) -> int:
        return self.item.state["position"]

    @property
    def is_opening(self) -> bool:
        return self.item.state["action"] == io.OutputShutterAction.UP

    @property
    def is_closing(self) -> bool:
        return self.item.state["action"] == io.OutputShutterAction.DOWN

    @property
    def is_closed(self) -> bool:
        return self.item.state["position"] == 0

    def open_cover(self, **kwargs):
        self.item.up()
        self.schedule_update_ha_state()

    def close_cover(self, **kwargs):
        self.item.down()
        self.schedule_update_ha_state()

    def set_cover_position(self, **kwargs):
        if ATTR_POSITION in kwargs:
            position = kwargs[ATTR_POSITION]
            self.item.set(position)
        self.schedule_update_ha_state()

    def stop_cover(self, **kwargs):
        self.item.stop()
        self.schedule_update_ha_state()


mapping = {
    io.OutputShutterSmart: OutputShutterSmart,
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities(
        setup_entities(hass, config_entry.entry_id, mapping, Platform.COVER)
    )
