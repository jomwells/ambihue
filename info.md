# Philips TV Ambilight+Hue (Switch) Component
A Switch component for automating the control of the Ambilight+hue setting on a Philips TV, this reveals the current status of the menu setting to Home Assistant, and allows for remote or automated toggling.
## Configuration

If you have already set up the Ambilight (Light) component, configuring this component is very simple, enter the same username and password as for the ambilight component in the configuration.yaml, along with the IP of the TV, and restart home assistant:

If you have not configured any other Philips TV components, use the tool linked in the [Ambilight (Light) component](https://github.com/jomwells/ambilights) GitHub docs to obtain your username and password.
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
