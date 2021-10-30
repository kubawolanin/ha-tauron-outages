"""TauronOutagesEntity class"""
from __future__ import annotations

from typing import Any

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import TauronOutagesDataUpdateCoordinator
from .const import (
    ATTRIBUTION,
    DOMAIN,
    NAME,
    VERSION,
    CONFIGURATION_URL,
    CONF_REVERSE_GEOCODE,
    RESPONSE_CURRENT_OUTAGES,
    RESPONSE_FUTURE_OUTAGES,
)


class TauronOutagesEntity(CoordinatorEntity):
    """Base TauronOutages entity."""

    coordinator: TauronOutagesDataUpdateCoordinator

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID to use for this entity."""
        if not self.coordinator.config_entry:
            return None
        return self.coordinator.config_entry.entry_id

    @property
    def device_info(self) -> DeviceInfo:
        road = (
            self.coordinator.config_entry.data[CONF_REVERSE_GEOCODE]
            .get("address")
            .get("road")
        )
        return DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=road,
            model=VERSION,
            manufacturer=NAME,
            configuration_url=CONFIGURATION_URL,
            attribution=ATTRIBUTION,
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "current_outages": str(self.coordinator.data.get(RESPONSE_CURRENT_OUTAGES)),
            "future_outages": str(self.coordinator.data.get(RESPONSE_FUTURE_OUTAGES)),
            "integration": DOMAIN,
        }
