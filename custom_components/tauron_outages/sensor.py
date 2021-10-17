"""Sensor platform for tauron_outages."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .entity import TauronOutagesEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([TauronOutagesSensor(coordinator)])


class TauronOutagesSensor(TauronOutagesEntity, SensorEntity):
    """tauron_outages Sensor class."""

    _attr_name = f"{DEFAULT_NAME}_{SENSOR}"
    _attr_icon = ICON

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data.get("address").get("postcode")
