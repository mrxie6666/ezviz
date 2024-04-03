# custom_components/ezviz/client.py
import requests
import json

EZVIZ_API_BASE_URL = "https://open.ys7.com/api/lapp/"

class EzvizClient:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = None
        self.refresh_token = None
        self.expires_in = 0

    def authenticate(self):
        url = f"{EZVIZ_API_BASE_URL}login/token"
        params = {
            "appKey": self.app_key,
            "appSecret": self.app_secret,
        }

        response = requests.post(url, params=params)
        data = response.json()

        if response.status_code != 200 or data["error"] != 0:
            raise Exception(f"Authentication failed: {data.get('msg')}")

        self.access_token = data["accessToken"]
        self.refresh_token = data["refreshToken"]
        self.expires_in = data["expiresIn"]

    def get_device_list(self):
        url = f"{EZVIZ_API_BASE_URL}device/list"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code != 200 or data["error"] != 0:
            raise Exception(f"Get device list failed: {data.get('msg')}")

        return data["devices"]

    def get_device_status(self, device_sn):
        url = f"{EZVIZ_API_BASE_URL}device/info?deviceSerial={device_sn}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code != 200 or data["error"] != 0:
            raise Exception(f"Get device status failed: {data.get('msg')}")

        return data["device"]