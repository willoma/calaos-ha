# Home Assistant Integration for Calaos

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=willoma&repository=calaos-ha&category=integration)

[Calaos](https://www.calaos.fr/) is a home automation platform, initially created with support of Wago 750 series PLCs.

This integration allows getting Calaos inputs and outputs states into Home Assistant, as well as triggering Calaos outputs.

Calaos configuration cannot be changed using Home Assistant.

## Notice

This integration is an independent project: the Calaos team is by no means invovled in its development.

## Calaos to Home Assistant mapping

A device is created for each Calaos supported item, as well as an entity when applicable.

As a general rule:

- items that only send one-shot events have no entity, only device triggers
  (buttons, switches, etc)
- items that only have values but cannot be modified are mapped to sensors or
  binary sensors
- items that can be modified/triggered are mapped to relevant types

The following devices/items from Calaos are supported:

| Calaos type     | HA platform     |
| --------------- | --------------- |
| **Generic**     |
| InPlageHoraire  | Binary sensor   |
| InputTime       | (triggers only) |
| InternalBool    | Switch          |
| InternalInt     | Number          |
| InternalString  | Text            |
| Scenario        | Switch          |
| **Wago**        |
| WIDigitalBP     | (triggers only) |
| WIDigitalLong   | (triggers only) |
| WIDigitalTriple | (triggers only) |
| WODali          | Light           |
| WODigital       | Light or switch |
| WOVoletSmart    | Cover           |
| **Web**         |
| WebInputAnalog  | Sensor          |
| WebInputString  | Sensor          |
| WebInputTemp    | Sensor          |
| **Fallback**    |
| Any other type  | Sensor          |

Calaos rooms are suggested as Home Assistant areas.

## Make lights be switches

At least in the Calaos version I am using right now, there is no way to define
outputs other than lights.

As a trick to make Calaos lights become switches in Home Assistant, use the
following prefixes in their name:

- `SW` for regular switches
- `OU` for outlets

That way, Calaos output lights will be seen as switches. The prefix is removed
in the entity and device name. Therefore, a Calaos light item with name
"SW Door" would be seen as a switch named "Door".

## Make digital input switches be sensors

In some situations, a Calaos digital input is not a button, but a binary sensor.
For instance, a movement sensor may be used as a Wago Digital Input.

As a trick to make Calaos inputs become binary sensors in Home Assistant, use
the following prefixes in their name:

- `BIN` for generic binary sensors
- `BIN:<class>` for specific binary sensors, where `<class>` is replaced with a
  class name (see
  <https://www.home-assistant.io/integrations/binary_sensor/#device-class>)

For instance, a digital input switch named "BIN:motion Hallway movement" would
be seen as a motion binary sensor with name "Hallway movement".
