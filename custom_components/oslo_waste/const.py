"""Oslo waste constants."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

BASEURL = 'https://www.oslo.kommune.no/avfall-og-gjenvinning/avfallshenting/'

ATTR_PICKUP_DATE = 'pickup_date'
ATTR_PICKUP_FREQUENCY = 'pickup_frequency'
ATTR_ADDRESS = 'address'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required('address'): cv.string,
    vol.Optional('street'): cv.string,
})