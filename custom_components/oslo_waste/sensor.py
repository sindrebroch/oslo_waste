from datetime import date, datetime
from homeassistant.components.sensor import ENTITY_ID_FORMAT, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_FRIENDLY_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import slugify

from custom_components.oslo_waste.models import HentePunkt, ResponseResult, Tjeneste

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

    for address in coordinator.addresses:
        for hentepunkt in address.HentePunkts:
            for tjeneste in hentepunkt.Tjenester:
                async_add_entities(
                    [OsloWasteSensor(coordinator, address, hentepunkt, tjeneste)]
                )


class OsloWasteSensor(SensorEntity):
    """Oslo Waste Sensor."""

    def __init__(
        self,
        coordinator: OsloWasteCoordinator,
        address: ResponseResult,
        hentepunkt: HentePunkt,
        tjeneste: Tjeneste,
    ):
        self._coordinator = coordinator
        self.address = address
        self.hentepunkt = hentepunkt
        self.tjeneste = tjeneste

        address_str = (
            self.address.Gatenavn
            + " "
            + str(self.address.Husnummer)
            + self.address.Bokstav
        )
        waste_type = tjeneste.Fraksjon.Tekst

        self._attributes = {
            ATTR_ADDRESS: address_str,
            ATTR_FRIENDLY_NAME: waste_type,
        }
        self.entity_slug = f"{address_str} {waste_type}"
        self.entity_id = ENTITY_ID_FORMAT.format(
            slugify(self.entity_slug.replace(" ", "_"))
        )
        self._attr_unique_id = self.entity_slug.replace(" ", "_")

        self._attr_icon = "mdi:trash-can"
        self._attr_unit_of_measurement = "days"
        self._attr_name = waste_type.title()

        self._attr_device_info = DeviceInfo(
            name="Oslo Waste",
            manufacturer="www.oslo.kommune.no",
            model=f"{address_str}",
            identifiers={(DOMAIN, address_str)},
            configuration_url="https://www.oslo.kommune.no/avfall-og-gjenvinning/nar-hentes-avfallet/",
        )

        self._state = None

        self.set_values()

    @property
    def native_value(self) -> StateType:
        if self._state is not None:
            return (self._state - date.today()).days

    @property
    def extra_state_attributes(self):
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

        self.set_values()

    def set_values(self):
        """Set sensor values."""
        pickup_date = self.tjeneste.TommeDato

        self._attributes[ATTR_PICKUP_DATE] = pickup_date
        self._attributes[ATTR_PICKUP_FREQUENCY] = self.tjeneste.Hyppighet.Tekst

        if pickup_date is not None:
            self._state = datetime.strptime(pickup_date, "%d.%m.%Y").date()
