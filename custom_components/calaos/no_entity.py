import logging

from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE

from pycalaos.item import io

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

triggers = {
    io.InputSwitch: {
        True: "click",
    },
    io.InputSwitchLongPress: {
        io.InputSwitchLongPressState.SHORT: "short_click",
        io.InputSwitchLongPressState.LONG: "long_click",
    },
    io.InputSwitchTriple: {
        io.InputSwitchTripleState.SINGLE: "single_click",
        io.InputSwitchTripleState.DOUBLE: "double_click",
        io.InputSwitchTripleState.TRIPLE: "triple_click",
    },
    io.InputTime: {
        True: "triggered",
    },
}


def all_triggers() -> set[str]:
    triggers_list = set()
    for this_triggers in triggers.values():
        for trigger_string in this_triggers.values():
            triggers_list.add(trigger_string)
    _LOGGER.debug(f"No-entity triggers: {triggers_list}")
    return triggers_list


def get_triggers(item_type, device_id: str) -> list[dict[str, str]]:
    if item_type not in triggers:
        return []
    item_triggers = []
    for trigger_string in triggers[item_type].values():
        item_triggers.append(
            {
                CONF_PLATFORM: "device",
                CONF_DOMAIN: DOMAIN,
                CONF_DEVICE_ID: device_id,
                CONF_TYPE: trigger_string,
            }
        )
    _LOGGER.debug(f"Triggers for {item_type}: {item_triggers}")
    return item_triggers


def translate_trigger(event) -> str:
    for itemType, itemTriggers in triggers.items():
        if isinstance(event.item, itemType):
            if event.state in itemTriggers:
                return itemTriggers[event.state]
            return None
    return None
