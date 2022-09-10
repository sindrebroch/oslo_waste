"""Oslo waste constants."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

PLATFORMS = ["sensor"]
DOMAIN = "oslo_waste"
NAME = f"{DOMAIN}"
VERSION = "3.0.0"
ISSUE_URL = "https://github.com/sindrebroch/oslo_waste/issues"

# API
BASEURL = "https://www.oslo.kommune.no/xmlhttprequest.php?service=ren.search"

# Attributes
ATTR_PICKUP_DATE = "pickup_date"
ATTR_PICKUP_FREQUENCY = "pickup_frequency"
ATTR_ADDRESS = "address"

# Config
CONF_STREET = "street"
CONF_NUMBER = "number"
CONF_LETTER = "letter"
CONF_STREET_ID = "street_id"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
