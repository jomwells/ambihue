[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![paypalme_badge](https://img.shields.io/badge/Donate-PayPal-0070ba)](https://paypal.me/MrGroch)
[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/MrGroch)

# Philips TV Ambilight+Hue (Switch) Component
A Switch component for automating the control of the Ambilight+hue setting on a Philips TV, this reveals the current status of the menu setting to Home Assistant, and allows for remote or automated toggling.

Forked from not maintained for a long time jomwell's repo:
https://github.com/jomwells/ambihue

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be installed using HACS. To do it search for `Philips Ambilight+Hue Switch` in Integrations section.

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `philips_ambilight_hue`.
4. Download _all_ the files from the `custom_components/philips_ambilight_hue/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant.
7. [Configure](#Configuration) custom component using Config Flow UI.


## Configuration

After installation of the custom component, it needs to be added using **Config Flow UI**.

To configure this integration go to: _Configuration_ -> _Integrations_ -> _Add integration_ -> _Philips TV Ambilight+Hue_.

You can also use following [My Home Assistant](http://my.home-assistant.io/) link

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=philips_ambilight_hue)

Configuration steps are similar to official Philips TV integration, so if you need help look [here](https://www.home-assistant.io/integrations/philips_js/).

*note:* there is often a noticeable lag between Home Assistant sending the request to toggle the setting, and receiving a status update from the API.
