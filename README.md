Ezviz Camera Integration for Home Assistant

This custom integration enables the connection between Home Assistant and an Ezviz camera, allowing users to view live streams and capture still images from their cameras within the Home Assistant environment. The integration supports specifying a camera channel number for multi-channel devices.

Code Structure

The code consists of two main parts:

Platform Setup

setup_platform: This function is called when the integration is initialized. It creates an instance of the EzvizCamera class and adds it to Home Assistant's list of available cameras.
EzvizCamera Class

EzvizCamera: Represents an individual Ezviz camera within Home Assistant. It extends the base Camera class provided by Home Assistant and implements various methods required for proper functionality.
Configuration

To use this integration, add the following configuration under the camera section in your configuration.yaml file:

yaml
camera:
  - platform: ezviz_camera
    id: <YOUR_DEVICE_SERIAL>
    Appkey: <YOUR_APPKEY>
    Secre: <YOUR_APPSECRET>
    name: <CAMERA_NAME>
    channel: <CHANNEL_NUMBER>  # Optional, defaults to 1; valid range: 1-4
Class Initialization (__init__)

When the EzvizCamera class is instantiated, it performs the following tasks:

Inherits properties and methods from the Camera base class.
Extracts configuration parameters such as the device serial, app key, app secret, camera name, and channel number.
Sets the unique ID for the camera entity using the camera name and device serial.
Initializes variables related to authentication tokens and motion status.
Methods

Authentication

get_token: Requests an access token from the Ezviz API using the provided app key and app secret. If successful, stores the access token and its expiration time in the respective class attributes.
Token Management

check_token_is_expired: Checks if the current access token has expired or is about to expire (within 1 second). Returns True if a new token is needed, False otherwise.
Image Capture

get_device_capture: Retrieves a still image from the specified camera channel using the current access token. Returns the URL of the captured image if successful, 'error' otherwise.
camera_image: Called by Home Assistant to fetch a still image from the camera. First checks if the access token needs to be refreshed, then calls get_device_capture. Handles any exceptions that may occur during the image retrieval process and returns the image content.
Live Stream

mjpeg_stream: Generates an HTTP MJPEG stream from the camera. Constructs the stream URL using the access token, device serial, and specified channel number. Yields the stream URL so that Home Assistant can handle the streaming process.
Properties

name: Returns the configured name of the camera.
supported_features: Specifies that the camera supports live streaming (CameraEntityFeature.STREAM).
should_poll: Indicates that the camera entity should be polled periodically by Home Assistant for updates.
Conclusion

This custom integration provides a basic framework for integrating an Ezviz camera into Home Assistant, supporting both live streaming and still image capture. Users can specify a camera channel number to interact with multi-channel devices. Ensure the provided app key, app secret, and device serial are accurate, and monitor Home Assistant logs for any issues during the integration's operation.
