from datetime import date
from homeassistant.components.sensor import (
    ENTITY_ID_FORMAT,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION, ATTR_FRIENDLY_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import slugify

from .coordinator import OsloWasteCoordinator
from .const import ATTR_ADDRESS, ATTR_PICKUP_DATE, ATTR_PICKUP_FREQUENCY, DOMAIN, LOGGER


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""

    coordinator: OsloWasteCoordinator = hass.data[DOMAIN][entry.entry_id]

    await coordinator.async_update()
    waste_types = await coordinator.waste_types()
        
    async_add_entities(
        OsloWasteSensor(coordinator, waste_type) for waste_type in waste_types
    )


class OsloWasteSensor(SensorEntity):
    def __init__(
        self,
        coordinator: OsloWasteCoordinator,
        waste_type: str,
    ):
        self._coordinator = coordinator
        self._waste_type = waste_type

        self._attributes = {
            ATTR_ADDRESS: self._coordinator.address,
            ATTR_FRIENDLY_NAME: self._waste_type,
        }
        self.entity_slug = f"{self._coordinator.address} {self._waste_type}"
        self.entity_id = ENTITY_ID_FORMAT.format(
            slugify(self.entity_slug.replace(" ", "_"))
        )
        self._attr_unique_id = self.entity_slug.replace(" ", "_")

        self._attr_icon = "mdi:trash-can"
        self._attr_unit_of_measurement = "days"
        self._attr_name = waste_type.title()

        self._state = None

    @property
    def native_value(self) -> StateType:
        if self._state is not None:
            return (self._state - date.today()).days

    @property
    def device_state_attributes(self) -> dict:
        return self._attributes

    async def async_update(self):
        """
        Ask scraper for new data if the current pickup date has passed or
        missing.
        """
        if self._state is not None:
            if (self._state - date.today()).days > 0:
                LOGGER.debug("%s - Skipping update.", self.entity_slug)
                return
        await self._coordinator.async_update()

        pickup_date = await self._coordinator.get_waste(self._waste_type)
        LOGGER.debug("pickup date %s", pickup_date)
        pickup_date = pickup_date.get("date")

        frequency = await self._coordinator.get_waste(self._waste_type)
        frequency = frequency.get("frequency")

        self._attributes[ATTR_PICKUP_DATE] = pickup_date.isoformat()
        self._attributes[ATTR_PICKUP_FREQUENCY] = frequency
        self._attributes[ATTR_ATTRIBUTION] = "Data is provided by www.oslo.kommune.no"
        if pickup_date is not None:
            self._state = pickup_date
