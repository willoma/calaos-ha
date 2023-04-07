import voluptuous as vol

from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers import device_registry
from homeassistant.helpers.config_validation import TRIGGER_BASE_SCHEMA
from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, EVENT_DOMAIN

TRIGGER_TYPES = {
    "click",
    "single_click", "double_click", "triple_click",
    "short_click", "long_click"
}

TRIGGER_SCHEMA = TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, str]]:
    dev_registry = device_registry.async_get(hass)
    device = dev_registry.async_get(device_id)
    entry_id = next(iter(device.config_entries))

    coordinator = hass.data[DOMAIN][entry_id]
    item_type = coordinator.item_type_by_device_id[device_id]

    if item_type == "switch":
        return switch_triggers(device_id)
    if item_type == "switch3":
        return switch3_triggers(device_id)
    if item_type == "switch_long":
        return switch_long_triggers(device_id)
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
