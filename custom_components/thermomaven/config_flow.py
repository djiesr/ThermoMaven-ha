"""Config flow for ThermoMaven integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, DEFAULT_APP_KEY, DEFAULT_APP_ID
from .thermomaven_api import ThermoMavenAPI

_LOGGER = logging.getLogger(__name__)

CONF_REGION = "region"

REGIONS = {
    "US": "United States / Canada",
    "DE": "Europe (Germany, UK, France...)",
    "CA": "Canada (alternative)",
}

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_REGION, default="US"): vol.In(REGIONS),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    api = ThermoMavenAPI(
        hass,
        data[CONF_EMAIL],
        data[CONF_PASSWORD],
        DEFAULT_APP_KEY,
        DEFAULT_APP_ID,
        region=data.get(CONF_REGION, "US"),
    )

    try:
        result = await api.async_login()
        if not result or result.get("code") != "0":
            raise InvalidAuth
    except Exception as err:
        _LOGGER.error("Failed to login: %s", err)
        raise CannotConnect from err

    region_name = REGIONS.get(data.get(CONF_REGION, "US"), "US")
    return {
        "title": f"ThermoMaven ({data[CONF_EMAIL]}) - {region_name}",
        "user_id": result["data"]["userId"],
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ThermoMaven."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Set unique ID to prevent duplicate entries
                await self.async_set_unique_id(user_input[CONF_EMAIL])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=info["title"],
                    data={
                        **user_input,
                        "app_key": DEFAULT_APP_KEY,
                        "app_id": DEFAULT_APP_ID,
                        "region": user_input.get(CONF_REGION, "US"),
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

