"""Binary sensor platform for tauron_outages."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    LOGGER,
    BINARY_SENSOR,
    BINARY_SENSOR_DEVICE_CLASS,
    DEFAULT_NAME,
    DOMAIN,
    RESPONSE_CURRENT_OUTAGES,
)
from .entity import TauronOutagesEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([TauronOutagesBinarySensor(coordinator)])


class TauronOutagesBinarySensor(TauronOutagesEntity, BinarySensorEntity):
    """tauron_outages binary_sensor class."""

    _attr_name = f"{DEFAULT_NAME}_{BINARY_SENSOR}"
    _attr_device_class = BINARY_SENSOR_DEVICE_CLASS

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        LOGGER.info(self.coordinator.data)
        return not len(self.coordinator.data[RESPONSE_CURRENT_OUTAGES]) > 0
