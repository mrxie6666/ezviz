import os
import time
import datetime
import requests
import logging
import voluptuous as vol
from homeassistant.components.camera import Camera, PLATFORM_SCHEMA
from voluptuous import Any, Optional, All, In, Range, MultipleInvalid
from homeassistant.components.camera import CameraEntityFeature
from homeassistant.const import CONF_CHANNEL  # 引入CONF_CHANNE

_LOGGER = logging.getLogger(__name__)

CONF_ID = 'id'
CONF_KEY = 'Appkey'
CONF_SEC = 'Secre'
CONF_NAME = 'name'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ID): str,
    vol.Required(CONF_KEY): str,
    vol.Required(CONF_SEC): str,
    vol.Required(CONF_NAME): str,
    vol.Optional(CONF_CHANNEL, default=1): vol.All(vol.Coerce(int), vol.Range(min=1, max=4)), 
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Ezviz camera platform."""
    add_devices([EzvizCamera(hass, config)])

class EzvizCamera(Camera):
    """Representation of an Ezviz camera."""
    def __init__(self, config_entry, device_info):
        super().__init__()
        self._config_entry = config_entry
        self._device_info = device_info
        self._channel = config_entry.data.get(CONF_CHANNEL)  # 添加通道号属性
           
    def __init__(self, hass, config):
        """Initialize an Ezviz camera."""
        super().__init__()

        self._parent = hass
        self._name = config[CONF_NAME]
        self._motion_status = False

        self.appKey = config[CONF_KEY]
        self.appSecret = config[CONF_SEC]
        self.accessToken = ""
        self.deviceSerial = config[CONF_ID]
        self.expireTime = 0

        self._attr_unique_id = self._name + self.deviceSerial

    def get_token(self):
        r = requests.post('https://open.ys7.com/api/lapp/token/get', data={
            'appKey': self.appKey,
            'appSecret': self.appSecret
        })
        token_result = r.json()

        if token_result['code'] == '200':
            self.accessToken = token_result['data']['accessToken']
            self.expireTime = token_result['data']['expireTime']
            return True
        else:
            return False

    def check_token_is_expired(self):
        now = int(round(time.time() * 1000))
        return now > (self.expireTime - 1000)

    def get_device_capture(self):
        r = requests.post('https://open.ys7.com/api/lapp/device/capture', data={
            'accessToken': self.accessToken,
            'deviceSerial': self.deviceSerial,
            'channelNo': 1,
            'quality': 1
        })
        result = r.json()

        if result['code'] == '200':
            return result['data']['picUrl']
        else:
            return 'error'

    def camera_image(self, width: int, height: int):
        """Return a still image response."""
        if self.check_token_is_expired():
            if not self.get_token():
                _LOGGER.error("Failed to get access token")
                return None

        image_path = self.get_device_capture()

        if image_path == 'error':
            return None

        try:
            response = requests.get(image_path)
        except requests.exceptions.RequestException as error:
            _LOGGER.error("Error getting camera image: %s", error)
            return None

        return response.content

    def mjpeg_stream(self):
        """Generate an HTTP MJPEG stream from the camera."""
        url = f'https://open.ys7.com/api/lapp/live/view?accessToken={self.accessToken}&deviceSerial={self.deviceSerial}'
        yield open_url(url)

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name

    @property
    def supported_features(self):
        return CameraEntityFeature.STREAM

    @property
    def should_poll(self):
        """Camera should poll periodically."""
        return True