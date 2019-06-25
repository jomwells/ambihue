# Phillips TV Ambilight+Hue (Switch) Component
For automating the control of the Ambilight+hue setting, use the additional Ambihue (Switch) component, this enables the status of the setting to be determined by Home Assistant, and allows for remote or automated toggling.
## Installation
If you have already set up the [Ambilight component](https://github.com/jomwells/ambilights), installing this switch component is very simple, copy the ```phillips_ambihue```  directory into your ```config/custom_components/``` directory,
enter the same username and password as for the ambilight component in the configuration.yaml as follows:
```
switch:
  - platform: philips_ambihue
    name: Ambilight+hue
    host: 192.168.1.XXX
    username: !secret philips_username
    password: !secret philips_password
    scan_interval: 5
```
*note* there is often a noticeable lag between Home Assistant sending the request to toggle the setting, and receiving a status update from the API, for this reason, it is advised that you reduce your `scan_interval` (in seconds) to suit your needs.
