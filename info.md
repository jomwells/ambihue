# Philips TV Ambilight+Hue (Switch) Component

A Switch component for automating the control of the Ambilight+hue setting on a Philips TV, this reveals the current status of the menu setting to Home Assistant, and allows for remote or automated toggling.

## Configuration

After installation of the custom component, it needs to be configured in `configuration.yaml` file.

If you have not configured any other Philips TV components, use [this tool](https://github.com/suborb/philips_android_tv) to obtain your username and password.
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
