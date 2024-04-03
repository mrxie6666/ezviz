from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_APP_KEY, CONF_APP_SECRET, CONF_DEVICE_SN
import homeassistant.helpers.config_validation as cv
from .sensor import EzvizSensor

async def async_setup_entry(hass, config_entry):
    """Set up the Ezviz integration from a config entry."""
    app_key = config_entry.data[CONF_APP_KEY]
    app_secret = config_entry.data[CONF_APP_SECRET]
    device_sn = config_entry.data[CONF_DEVICE_SN]

    # 实例化EzvizClient类，并完成初始化
    client = EzvizClient(app_key, app_secret)
    client.authenticate()

    # 实例化EzvizSensor类，并完成初始化
    sensor = EzvizSensor(client, device_sn)

    # 注册传感器到Home Assistant
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    return True


CONFIG_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_APP_KEY): cv.string,
        vol.Required(CONF_APP_SECRET): cv.string,
        vol.Required(CONF_DEVICE_SN): cv.string,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Ezviz platform."""
    if discovery_info is not None:
        app_key = discovery_info["app_key"]
        app_secret = discovery_info["app_secret"]
        device_sn = discovery_info["device_sn"]
    else:
        app_key = config[CONF_APP_KEY]
        app_secret = config[CONF_APP_SECRET]
        device_sn = config[CONF_DEVICE_SN]

    # 创建并添加传感器实体到Home Assistant
    async_add_entities([EzvizSensor(EzvizClient(app_key, app_secret), device_sn)])
