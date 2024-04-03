
# custom_components/ezviz/sensor.py
import logging
from datetime import timedelta
import asyncio
from homeassistant.helpers.entity import Entity
from homeassistant.util.dt import utcnow

from .client import EzvizClient

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

class EzvizSensor(Entity):
    """Implementation of an Ezviz Sensor."""

    def __init__(self, ezviz_client, device_sn):
        """Initialize the sensor."""
        self._state = None
        self._device_sn = device_sn
        self._attrs = {}
        self._ezviz_client = ezviz_client

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Ezviz Device {self._device_sn}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return additional attributes for the sensor."""
        return self._attrs

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:camera"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "Status"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            device_status = self._ezviz_client.get_device_status(self._device_sn)
            self._state = device_status["online"]  # 假设设备状态中包含名为"online"的在线状态字段
            self._attrs.update(device_status)  # 更新其他可能需要展示的属性
        except Exception as ex:
            _LOGGER.error("Error fetching Ezviz device status: %s", ex)
            self._state = "Error"
