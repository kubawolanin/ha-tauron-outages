"""Adds config flow for TauronOutages."""
from __future__ import annotations
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import TauronOutagesApiClient
from .const import (
    LOGGER,
    CONF_LONGITUDE,
    CONF_LATITUDE,
    CONF_REVERSE_GEOCODE,
    CONF_CITY_GAID,
    CONF_STREET_GAID,
    DOMAIN,
    PLATFORMS,
)


class TauronOutagesFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for TauronOutages."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ):
        """Handle a flow initialized by the user."""
        errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            lat = user_input[CONF_LATITUDE]
            lon = user_input[CONF_LONGITUDE]
            session = async_create_clientsession(self.hass)
            client = TauronOutagesApiClient(lat, lon, session)
            reverse_geocode = await self._get_reverse_geocode(client)
            if reverse_geocode:
                user_input[CONF_REVERSE_GEOCODE] = reverse_geocode

                city_gaid_response = await self._get_city_gaid(client, reverse_geocode)

                if city_gaid_response:
                    # city_gaid = city_gaid_response[0]["Gaid"]
                    city_gaid = city_gaid_response.get("userId")
                    LOGGER.info(city_gaid)
                    user_input[CONF_CITY_GAID] = city_gaid
                    street_gaid_response = await self._get_street_gaid(
                        client, reverse_geocode, city_gaid
                    )

                    if street_gaid_response:
                        street_gaid = street_gaid_response.get("userId")
                        # street_gaid = street_gaid_response[0].get("Gaid")
                        LOGGER.info(street_gaid)
                        user_input[CONF_STREET_GAID] = street_gaid
                        return self.async_create_entry(
                            title=reverse_geocode.get("address").get("road"),
                            data=user_input,
                        )
                    else:
                        errors["base"] = "street_gaid"
                else:
                    errors["base"] = "city_gaid"
            else:
                errors["base"] = "reverse_geocode"

        if user_input is None:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_LATITUDE,
                        default=user_input.get(
                            CONF_LATITUDE, self.hass.config.latitude
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=-89, max=89)),
                    vol.Required(
                        CONF_LONGITUDE,
                        default=user_input.get(
                            CONF_LONGITUDE, self.hass.config.longitude
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=-180, max=180)),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return TauronOutagesOptionsFlowHandler(config_entry)

    async def _get_reverse_geocode(self, client: TauronOutagesApiClient):
        """Return true if credentials is valid."""
        try:
            return await client.async_get_reverse_geocode()
        except Exception:  # pylint: disable=broad-except
            pass
        return False

    async def _get_city_gaid(
        self, client: TauronOutagesApiClient, reverse_geocode: Any
    ):
        """Return true if credentials is valid."""
        try:
            return await client.async_get_city_gaid(reverse_geocode)
        except Exception:  # pylint: disable=broad-except
            pass
        return False

    async def _get_street_gaid(
        self, client: TauronOutagesApiClient, reverse_geocode: Any, city_gaid: Any
    ):
        """Return true if credentials is valid."""
        try:
            return await client.async_get_street_gaid(reverse_geocode, city_gaid)
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class TauronOutagesOptionsFlowHandler(config_entries.OptionsFlow):
    """TauronOutages config flow options handler."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=self.config_entry.data.get(CONF_LATITUDE),
                data=self.options,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )
