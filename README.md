[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![paypalme_badge](https://img.shields.io/badge/Donate-PayPal-0070ba?style=flat)](https://paypal.me/MrGroch)

# Philips TV Ambilight+Hue (Switch) Component
A Switch component for automating the control of the Ambilight+hue setting on a Philips TV, this reveals the current status of the menu setting to Home Assistant, and allows for remote or automated toggling.

Forked from not maintained for a long time jomwell's repo:
https://github.com/jomwells/ambihue

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be added to HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories):
* URL: `https://github.com/Mr-Groch/ambihue`
* Category: `Integration`

After adding a custom repository you can use HACS to install this integration using user interface.

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `philips_ambilight+hue`.
4. Download _all_ the files from the `custom_components/philips_ambilight+hue/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. [Configure](#Configuration) custom component in `configuration.yaml` file.
7. Restart Home Assistant.

## Configuration

After installation of the custom component, it needs to be configured in `configuration.yaml` file.

If you have not setup any other Philips TV components, use the tool linked in the Ambilight (Light) component docs to obtain your username and password.
```
switch:
  - platform: philips_ambilight+hue
    name: Ambilight+Hue
    host: 192.168.1.XXX
    secured_transport: true
    api_version: 6
    username: !secret philips_username
    password: !secret philips_password
    scan_interval: 5
```

For older Philips TV try to change `secured_transport: false` (`username:` and `password:` is not required then). If this still doesn't help change also `api_version: 1`

*note:* there is often a noticeable lag between Home Assistant sending the request to toggle the setting, and receiving a status update from the API, for this reason, it is advised that you reduce your `scan_interval` (in seconds) to suit your needs.

