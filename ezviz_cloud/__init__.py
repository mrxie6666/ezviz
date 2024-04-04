

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ezviz_cloud"

CONF_APP_KEY = "app_key"
CONF_APP_SECRET = "app_secret"

DEFAULT_APP_KEY = "09bec3fd95f146c2b532bf6373500efc"
DEFAULT_APP_SECRET = "9f0af52d2e70ed23be36444ff69a899b"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_APP_KEY, default=DEFAULT_APP_KEY): cv.string,
        vol.Optional(CONF_APP_SECRET, default=DEFAULT_APP_SECRET): cv.string,
    }
)

async def async_setup(hass, config):
    """Set up the Ezviz Cloud component."""
    from .sensor import EzvizCloudSensor

    hass.data[DOMAIN] = {}
    conf = config[DOMAIN]

    # 实例化EzvizCloudSensor类并添加到HASS
    await hass.helpers.entity_component.async_add_entities(
        [EzvizCloudSensor(conf)], True
    )

    return True