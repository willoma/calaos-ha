"""Config flow for the Calaos integration."""

import logging
from typing import Any
from urllib.error import HTTPError

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_URL,
    CONF_USERNAME,
)
from homeassistant.data_entry_flow import FlowResult

from pycalaos import Client, discover

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def conf_schema(discovered_ip):
    return vol.Schema(
        {
            vol.Required(CONF_URL, default="https://" + discovered_ip): str,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        }
    )


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, info: dict[str, Any] | None = None) -> FlowResult:
        if info is None:
            discovered_ip = await self.hass.async_add_executor_job(discover, 1)
            return self.async_show_form(
                step_id="user", data_schema=conf_schema(discovered_ip)
            )

        errors = {}
        try:
            await self.hass.async_add_executor_job(
                Client, info["url"], info["username"], info["password"]
            )
        except HTTPError:
            errors["base"] = "invalid_auth"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title="Calaos", data=info)

        discovered_ip = await self.hass.async_add_executor_job(discover, 1)
        return self.async_show_form(
            step_id="user", data_schema=conf_schema(discovered_ip), errors=errors
        )
