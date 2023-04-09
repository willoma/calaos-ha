# Home Assistant Integration for Calaos

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tiramiseb&repository=calaos-ha&category=integration)

[Calaos](https://www.calaos.fr/) is a home automation platform, initially created with support of Wago 750 series PLCs.

This integration allows getting Calaos inputs and outputs states into Home Assistant, as well as triggering Calaos outputs.

Calaos configuration cannot be changed using Home Assistant.

## Notice

This integration is an independent project: the Calaos team is by no means invovled in its development.

## Calaos to Home Assistant mapping

A device is created for each Calaos supported item, as well as an entity when applicable.

The following devices/items from Calaos are supported:

| Device / item         | Calaos gui_type | HA entity platform |
|-----------------------|-----------------|--------------------|
| Button                | switch          | (trigger only)     |
| Triple-click button   | switch3         | (trigger only)     |
| Long-click button     | switch_long     | (trigger only)     |
| Relay (on/off lights) | light           | light or switch    |
| DALI light            | light_dimmer    | light              |
| Scenario              | scenario        | binary_sensor      |
| Time range            | time_range      | binary_sensor      |

Calaos rooms are suggested as Home Assistant areas.

## Make lights be switches

At least in the Calaos version I am using right now, there is no way to define
outputs other than lights.

As a trick to make Calaos lights become switches in Home Assistant, use the
following prefixes in their name:

- `SW` for regular switches
- `OU` for outlets

That way, outputs with Calaos `light` gui_type will be seen as switches. The
prefix is removed in the items names. Therefore, a Calaos light item with name
"SW Door" will be seen as a switch named "Door".
