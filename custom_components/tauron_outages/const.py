"""Constants for tauron_outages."""
from datetime import timedelta
from logging import Logger, getLogger

# Base component constants
NAME = "Tauron Outages"
DOMAIN = "tauron_outages"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ATTRIBUTION = "Data provided by TAURON Dystrybucja and TAURON Ciepło IAPI."
CONFIGURATION_URL = "https://www.tauron-dystrybucja.pl/wylaczenia/"
ISSUE_URL = "https://github.com/kubawolanin/ha-tauron-outages/issues"
DATA_COORDINATOR_UPDATE_INTERVAL = timedelta(hours=6)
LOGGER: Logger = getLogger(__package__)

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "power"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
PLATFORMS = [BINARY_SENSOR, SENSOR]

OUTAGE_TYPE_MAP = {1: "unplanned", 2: "planned"}

# Configuration and options
CONF_ENABLED = "enabled"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_REVERSE_GEOCODE = "reverse_geocode"
CONF_CITY_GAID = "city_gaid"
CONF_STREET_GAID = "street_gaid"

REVERSE_GEOCODE_URL = (
    "https://nominatim.openstreetmap.org/reverse.php?zoom=18&format=jsonv2"
)
POWER_URL = "https://www.tauron-dystrybucja.pl/iapi/"
HEAT_URL = "https://www.tauron-cieplo.pl/iapi/"

RESPONSE_CURRENT_OUTAGES = "CurrentOutagePeriods"
RESPONSE_FUTURE_OUTAGES = "FutureOutagePeriods"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
