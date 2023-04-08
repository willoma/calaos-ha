import voluptuous as vol

from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from homeassistant.components.binary_sensor.device_trigger import (
    async_get_triggers as binary_sensor_async_get_triggers,
    async_attach_trigger as binary_sensor_async_attach_trigger
)
from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.light import DOMAIN as LIGHT_DOMAIN
from homeassistant.components.light.device_trigger import (
    async_get_triggers as light_async_get_triggers,
    async_attach_trigger as light_async_attach_trigger
)
from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers import device_registry
from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, EVENT_DOMAIN

TRIGGER_TYPES = {
    "click",
    "single_click", "double_click", "triple_click",
    "short_click", "long_click"
}

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Optional(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, str]]:
    dev_registry = device_registry.async_get(hass)
    device = dev_registry.async_get(device_id)
    entry_id = next(iter(device.config_entries))
    dev_identifier = next(iter(device.identifiers))
    if len(dev_identifier) == 3:
        return await item_triggers(hass, device_id, entry_id, dev_identifier[2])
    if len(dev_identifier) == 2:
        # TODO triggers related to the calaos server itself
        pass
    return []


async def item_triggers(
    hass: HomeAssistant, device_id: str, entry_id: str, item_id: str
) -> list[dict[str, str]]:
    coordinator = hass.data[DOMAIN][entry_id]
    item = coordinator.item(item_id)

    if item.gui_type == "switch":
        return switch_triggers(device_id)
    if item.gui_type == "switch3":
        return switch3_triggers(device_id)
    if item.gui_type == "switch_long":
        return switch_long_triggers(device_id)
    if item.gui_type == "scenario" or item.gui_type == "time_range":
        return await binary_sensor_async_get_triggers(hass, device_id)
    if item.gui_type == "light" or item.gui_type == "light_dimmer":
        return await light_async_get_triggers(hass, device_id)
    return []


@callback
def switch_triggers(device_id: str) -> list[dict[str, str]]:
    return [
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: "click",
        }
    ]


@callback
def switch3_triggers(device_id: str) -> list[dict[str, str]]:
    return [
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: "single_click",
        },
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: "double_click",
        },
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: "triple_click",
        }
    ]


@callback
def switch_long_triggers(device_id: str) -> list[dict[str, str]]:
    return [
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: "short_click",
        },
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: "long_click",
        }
    ]


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    if config[CONF_DOMAIN] == LIGHT_DOMAIN:
        return await light_async_attach_trigger(hass, config, action, trigger_info)
    if config[CONF_DOMAIN] == BINARY_SENSOR_DOMAIN:
        return await binary_sensor_async_attach_trigger(hass, config, action, trigger_info)

    event_config = event_trigger.TRIGGER_SCHEMA({
        event_trigger.CONF_PLATFORM: "event",
        event_trigger.CONF_EVENT_TYPE: EVENT_DOMAIN,
        event_trigger.CONF_EVENT_DATA: {
            CONF_DEVICE_ID: config[CONF_DEVICE_ID],
            CONF_TYPE: config[CONF_TYPE],
        },
    })
    return await event_trigger.async_attach_trigger(
        hass, event_config, action, trigger_info, platform_type="device"
    )
