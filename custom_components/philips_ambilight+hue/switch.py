#import logging
import json
import string
import requests
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.switch import (
    DOMAIN, PLATFORM_SCHEMA, SwitchEntity, ENTITY_ID_FORMAT)
from homeassistant.const import (CONF_HOST, CONF_API_VERSION, CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_ID, STATE_OFF, STATE_STANDBY, STATE_ON)
from requests.auth import HTTPDigestAuth
from requests.adapters import HTTPAdapter

DEFAULT_DEVICE = 'default'
DEFAULT_HOST = '127.0.0.1'
DEFAULT_API_VERSION = 6
DEFAULT_SECURED_TRANSPORT = True
DEFAULT_USER = 'user'
DEFAULT_PASS = 'pass'
DEFAULT_NAME = 'Ambilight+Hue'
BASE_URL = '{0}://{1}:{2}/{3}/{4}'
TIMEOUT = 5.0
CONNFAILCOUNT = 5

#_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Required(CONF_API_VERSION, default=DEFAULT_API_VERSION): vol.In([1, 5, 6]),
    vol.Required('secured_transport', default=DEFAULT_SECURED_TRANSPORT): cv.boolean,
    vol.Required(CONF_USERNAME, default=DEFAULT_USER): cv.string,
    vol.Required(CONF_PASSWORD, default=DEFAULT_PASS): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    api_version = config.get(CONF_API_VERSION)
    secured_transport = config.get('secured_transport')
    user = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    add_devices([AmbiHue(name, host, api_version, secured_transport, user, password)])

class AmbiHue(SwitchEntity):

    def __init__(self, name, host, api_version, secured_transport, user, password):
        self._name = name
        self._host = host
        self._api_version = api_version
        if secured_transport:
            self._protocol = "https"
            self._port = 1926
        else:
            self._protocol = "http"
            self._port = 1925
        self._user = user
        self._password = password
        self._state = False
        self._connfail = 0
        self._available = False
        self._session = requests.Session()
        self._session.mount('https://', HTTPAdapter(pool_connections=1))

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def available(self):
        return self._available

    @property
    def should_poll(self):
        return True


    def turn_on(self, **kwargs):
        self._postReq('HueLamp/power', {"power":"On"}, True )
        self._state = True

    def turn_off(self, **kwargs):
        self._postReq('HueLamp/power', {"power":"Off"}, True )
        self._state = False

    def getState(self):
        fullstate = self._getReq('HueLamp/power')
        #_LOGGER.warn(fullstate)
        if fullstate:
            self._available = True
            ahstat = fullstate['power']
            if ahstat == 'On':
                self._state = True
            else:
                self._state = False
        else:
            self._available = False
            self._state = False

    def update(self):
        self.getState()

    def _getReq(self, path):
        try:
            if self._connfail:
                self._connfail -= 1
                return False
            resp = self._session.get(BASE_URL.format(self._protocol, self._host, self._port, self._api_version, path), verify=False, auth=HTTPDigestAuth(self._user, self._password), timeout=TIMEOUT)
            self.on = True
            return json.loads(resp.text)
        except requests.exceptions.RequestException as err:
            self._connfail = CONNFAILCOUNT
            self.on = False
            return False

    def _postReq(self, path, data, write):
        try:
            if self._connfail:
                self._connfail -= 1
                return False
            resp = self._session.post(BASE_URL.format(self._protocol, self._host, self._port, self._api_version, path), data=json.dumps(data), verify=False, auth=HTTPDigestAuth(self._user, self._password), timeout=TIMEOUT)
            #self.on = True
            if write:
                return True
            else:
                return json.loads(resp.text)
        except requests.exceptions.RequestException as err:
            self._connfail = CONNFAILCOUNT
            self.on = False
            return False
