"""
Custom integration to integrate tauron_outages with Home Assistant.

For more details about this integration, please refer to
https://github.com/kubawolanin/ha-tauron-outages
"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import TauronOutagesApiClient
from .const import (
    CONF_LONGITUDE,
    CONF_LATITUDE,
    DOMAIN,
    LOGGER,
    PLATFORMS,
    STARTUP_MESSAGE,
)
from .coordinator import TauronOutagesDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    LOGGER.info(STARTUP_MESSAGE)
    hass.data.setdefault(DOMAIN, {})

    api_client = TauronOutagesApiClient(
        latitude=entry.data[CONF_LATITUDE],
        longitude=entry.data[CONF_LONGITUDE],
        session=async_get_clientsession(hass),
    )

    coordinator = TauronOutagesDataUpdateCoordinator(hass, api=api_client)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )

    entry.add_update_listener(async_reload_entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, [platform for platform in PLATFORMS if platform in coordinator.platforms]
    ):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
