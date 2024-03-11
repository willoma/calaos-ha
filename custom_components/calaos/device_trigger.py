import logging

import voluptuous as vol

from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from homeassistant.components.binary_sensor.device_trigger import (
    async_get_triggers as binary_sensor_async_get_triggers,
    async_attach_trigger as binary_sensor_async_attach_trigger,
)
from homeassistant.components.cover import DOMAIN as COVER_DOMAIN
from homeassistant.components.cover.device_trigger import (
    async_get_triggers as cover_async_get_triggers,
    async_attach_trigger as cover_async_attach_trigger,
)
from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.components.light import DOMAIN as LIGHT_DOMAIN
from homeassistant.components.light.device_trigger import (
    async_get_triggers as light_async_get_triggers,
    async_attach_trigger as light_async_attach_trigger,
)
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.sensor.device_trigger import (
    async_get_triggers as sensor_async_get_triggers,
    async_attach_trigger as sensor_async_attach_trigger,
)
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.components.switch.device_trigger import (
    async_get_triggers as switch_async_get_triggers,
    async_attach_trigger as switch_async_attach_trigger,
)
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_TYPE
from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.helpers import device_registry
from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
from homeassistant.helpers.typing import ConfigType

from pycalaos.item import common, io

from .const import DOMAIN, EVENT_DOMAIN
from .no_entity import (
    all_triggers as noentity_all_triggers,
    get_triggers as noentity_get_triggers,
    triggers as noentity_triggers,
)
from .binary_sensor import is_a_binary_sensor
from .switch import is_a_switch

_LOGGER = logging.getLogger(__name__)

TRIGGER_TYPES = noentity_all_triggers()

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Optional(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)

attach_mapping = {
    BINARY_SENSOR_DOMAIN: binary_sensor_async_attach_trigger,
    COVER_DOMAIN: cover_async_attach_trigger,
    LIGHT_DOMAIN: light_async_attach_trigger,
    SENSOR_DOMAIN: sensor_async_attach_trigger,
    SWITCH_DOMAIN: switch_async_attach_trigger,
}


# Only entities in this list. For triggers without entities, see no_entity.py
get_mapping = {
    common.Default: sensor_async_get_triggers,
    io.InPlageHoraire: binary_sensor_async_get_triggers,
    io.InputAnalog: sensor_async_get_triggers,
    io.InputString: sensor_async_get_triggers,
    io.InputTemp: sensor_async_get_triggers,
    io.InternalBool: switch_async_get_triggers,
    io.OutputLightDimmer: light_async_get_triggers,
    io.OutputShutterSmart: cover_async_get_triggers,
    io.Scenario: switch_async_get_triggers,
}


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    # Existing domains
    for domain, attach in attach_mapping.items():
        if config[CONF_DOMAIN] == domain:
            _LOGGER.debug("Attaching trigger for %s", domain)
            return await attach(hass, config, action, trigger_info)

    # No-entity triggers
    event_config = event_trigger.TRIGGER_SCHEMA(
        {
            event_trigger.CONF_PLATFORM: "event",
            event_trigger.CONF_EVENT_TYPE: EVENT_DOMAIN,
            event_trigger.CONF_EVENT_DATA: {
                CONF_DEVICE_ID: config[CONF_DEVICE_ID],
                CONF_TYPE: config[CONF_TYPE],
            },
        }
    )
    _LOGGER.debug("Attaching trigger for no-entity device: %s", event_config)
    return await event_trigger.async_attach_trigger(
        hass, event_config, action, trigger_info, platform_type="device"
    )


async def item_triggers(
    hass: HomeAssistant, device_id: str, entry_id: str, item_id: str
) -> list[dict[str, str]]:
    coordinator = hass.data[DOMAIN][entry_id]
    item = coordinator.item(item_id)

    for item_type, get_triggers in get_mapping.items():
        if isinstance(item, item_type):
            return await get_triggers(hass, device_id)

    # Specific for lights, which can also be switches
    if isinstance(item, io.OutputLight):
        if is_a_switch(item):
            return await switch_async_get_triggers(hass, device_id)
        else:
            return await light_async_get_triggers(hass, device_id)

    # Specific for input buttons, which can also be binary sensors
    if isinstance(item, io.InputSwitch) and is_a_binary_sensor(item):
        return await binary_sensor_async_get_triggers(hass, device_id)

    # No-entity triggers
    for item_type in noentity_triggers.keys():
        if isinstance(item, item_type):
            return noentity_get_triggers(item_type, device_id)

    return []


async def async_get_triggers(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, str]]:
    dev_registry = device_registry.async_get(hass)
    device = dev_registry.async_get(device_id)
    entry_id = next(iter(device.config_entries))
    dev_identifier = next(iter(device.identifiers))
    if len(dev_identifier) == 3:
        triggers = await item_triggers(hass, device_id, entry_id, dev_identifier[2])
        _LOGGER.debug("Triggers for %s: %s", device_id, triggers)
        return triggers
    _LOGGER.debug("Wrong identifier: %s", dev_identifier)
    return []
