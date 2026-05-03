import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':     'database',
        'USER':     'user',
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST':     'database',
        'PORT':     '5432',
    }
}

# ALLOWED_HOSTS aus URL_HOST ableiten
_url_host = os.environ.get('URL_HOST', '')
if _url_host:
    from urllib.parse import urlparse
    _hostname = urlparse(_url_host).hostname
    if _hostname:
        ALLOWED_HOSTS = [_hostname]
else:
    ALLOWED_HOSTS = ['*']

EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True'

# LDAP
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

AUTH_LDAP_SERVER_URI = 'ldap://ldap:389/'
AUTH_LDAP_BIND_DN = 'cn=admin,dc=mind-hochschul-netzwerk,dc=de'
AUTH_LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD', '')

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'ou=people,dc=mind-hochschul-netzwerk,dc=de',
    ldap.SCOPE_SUBTREE,
    '(cn=%(user)s)',
)

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name':  'sn',
    'email':      'mail',
}
AUTH_LDAP_ALWAYS_UPDATE_USER = True

AUTHENTICATION_BACKENDS = [
    'helios_auth.auth_systems.ldapbackend.backend.CustomLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_ENABLED_SYSTEMS = ['ldap','password']

ALLOW_OPEN_REGISTRATION = False

HELIOS_ADMIN_ONLY = True
HELIOS_VOTERS_UPLOAD = False

DEFAULT_FROM_NAME = 'Wahlsystem von MHN'

SHOW_LOGIN_OPTIONS = False
SHOW_USER_INFO = False

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de-de'

SITE_TITLE = 'Wahlsystem von MHN'
WELCOME_MESSAGE = 'Herzlich willkommen zum Wahlsystem des Mind-Hochschul-Netzwerks!'
HELP_EMAIL_ADDRESS = 'wahl@mind-hochschul-netzwerk.de'


