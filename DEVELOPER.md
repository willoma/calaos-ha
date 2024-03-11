# Calaos-HA dev doc

## Supporting a new item type as an entity

First, select the platform for that entity
(see <https://developers.home-assistant.io/docs/core/entity/>).

If the platform is not already supported in Calaos-HA:

- Add a `xxx.py` file for this platform
- In `__init__.py`, add the platform in the `PLATFORMS` list
- In `device_trigger.py`, add the platform into the `attach_mapping` dictionary

Once the platform is chosen:

- Add a class in `xxx.py`, ideally with the same name as the item type
- Add the item in the `mapping` dictionary at the bottom of the file, or add
  a specific function to setup entities (to be called in `async_setup_entry`)
- In `device_trigger.py`, add the item to the `get_mapping` dictionary, or add
  some specific code in the `item_triggers` function
- In `README.md`, add the item/entity mapping into the table of the
  `Calaos to Home Assistant mapping` section

## Supporting a new item type as triggers only

If the item is just used to generate events (for instance, wall switches):

- In `no_entity.py`, add it to the `triggers` dictionary
- In `translations/*.json`, add translations for the added triggers
- In `README.md`, add the item into the table of the
  `Calaos to Home Assistant mapping` section

## Debug logging

In `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.calaos.binary_sensor: debug
    custom_components.calaos.config_flow: debug
    custom_components.calaos.coordinator: debug
    custom_components.calaos.device_trigger: debug
    custom_components.calaos.entity: debug
    custom_components.calaos.light: debug
    custom_components.calaos.no_entity: debug
    custom_components.calaos.switch: debug
    pycalaos.client: debug
    pycalaos.item: debug
    pycalaos.item.common: debug
```
