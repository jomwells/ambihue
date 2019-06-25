# Phillips TV Ambilight+Hue (Switch) Component
A Switch component for automating the control of the Ambilight+hue setting on a Phillips TV, this reveals the current status of the menu setting to Home Assistant, and allows for remote or automated toggling.
## Installation

#### Option 1: (recommended)
This repository is compatible with the Home Assistant Community Store ([HACS](https://community.home-assistant.io/t/custom-component-hacs/121727)).

After installing HACS, add the repository ```https://github.com/jomwells/ambihue```in settings, and use the ```configuration.yaml``` example below.

#### Option 2: (manual)
If you have already set up the [Ambilight (Light) component](https://github.com/jomwells/ambilights), installing this component is very simple, copy the ```philips_ambilight+hue``` directory into your ```config/custom_components/``` directory,
enter the same username and password as for the ambilight component in the configuration.yaml, along with the IP of the TV, and restart home assistant:

If you have not setup any other phillips TV components, use the tool linked in the Ambilight (Light) component docs to obtain your username and password.
```
switch:
  - platform: philips_ambihue
    name: Ambilight+hue
    host: 192.168.1.XXX
    username: !secret philips_username
    password: !secret philips_password
    scan_interval: 5
```

*note:* there is often a noticeable lag between Home Assistant sending the request to toggle the setting, and receiving a status update from the API, for this reason, it is advised that you reduce your `scan_interval` (in seconds) to suit your needs.
