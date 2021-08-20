"""Oslo waste constants."""

from logging import Logger, getLogger


from homeassistant.components.sensor import PLATFORM_SCHEMA

LOGGER: Logger = getLogger(__package__)

DOMAIN = "oslo_waste"
NAME = f"{DOMAIN}"
VERSION = "2.0.0"
ISSUE_URL = "https://github.com/kvisle/oslo_waste/issues"

# API
BASEURL = "https://www.oslo.kommune.no/avfall-og-gjenvinning/avfallshenting/"

# Attributes
ATTR_PICKUP_DATE = "pickup_date"
ATTR_PICKUP_FREQUENCY = "pickup_frequency"
ATTR_ADDRESS = "address"

# Config
CONF_ADDRESS = "address"
CONF_STREET = "street"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
