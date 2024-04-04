# ezviz
The manifest.json file provides metadata and configuration details about your Home Assistant custom component.

domain: The unique identifier for your integration, used internally by Home Assistant. In this case, it's set to "ezviz".

name: A human-readable name for your integration, displayed in the UI. Set to "Ezviz Integration".

version: The version number of your integration, following semantic versioning (e.g., 0.1.0). This helps users identify which version they are using and allows for easy updates.

documentation: A link to comprehensive documentation for your integration. Replace the placeholder URL with the actual URL of your GitHub repository's README file or dedicated documentation site.

issue_tracker: A link to where users can report issues or feature requests related to your integration. Typically, this points to the issue tracker of your GitHub repository.

dependencies: An array listing any required Home Assistant dependencies that must be installed for your integration to function correctly. Currently empty, but you may need to add dependencies if you use other Home Assistant components or libraries.

codeowners: A list of GitHub usernames or teams responsible for maintaining this integration. Replace @your-github-username with your actual GitHub username or team handle.

requirements: A list of Python packages required by your integration, specified as PyPI package names along with version constraints. In this example, we include "requests" with a version range of >=2.27.1,<3.0.0. Adjust this according to the actual requirements of your integration.

config_flow: Set to true to indicate that your integration uses a configuration flow (i.e., a user-friendly setup process within the Home Assistant UI). In our example, this would allow users to input their Ezviz credentials and configure devices through the UI rather than manually editing YAML files.

iot_class: Describes the communication pattern of your integration. "cloud_polling" indicates that your integration periodically polls a cloud service for updates. Other options might include "local_push" or "cloud_push" depending on how your integration communicates with devices.

is_built_in: Set to false since this is a custom integration developed outside of the core Home Assistant project. Built-in integrations would have this set to true.

This manifest.json file should be placed in the root directory of your custom component (custom_components/ezviz/) alongside the other Python modules (__init__.py, sensor.py, and client.py). Make sure to update the links and version numbers as needed when releasing new versions or making changes to your integration.

