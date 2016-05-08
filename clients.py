#!/usr/bin/env python
# Boilerplate for preparing client objects
import os, sys
from keystoneclient.exceptions import AuthorizationFailure, Unauthorized
from keystoneclient.v2_0 import client as kclient2
from urlparse import urlparse

_keystone_creds = {}
try:
    _keystone_creds['username'] = os.environ['OS_USERNAME']
    _keystone_creds['password'] = os.environ['OS_PASSWORD']
    _keystone_creds['auth_url'] = os.environ['OS_AUTH_URL']
    _keystone_creds['tenant_name'] = os.environ['OS_TENANT_NAME']
except KeyError, e:
    print ("Openstack environment variable %s is not set!") % e
    sys.exit(1)


# Evaluate the auth URL to determine if user is using v2 or v3 Keystone API
u = urlparse(_keystone_creds['auth_url'])

if "v2.0" in u.path:
    try:
	keystone = kclient2.Client(**_keystone_creds)
    except AuthorizationFailure as auf:
        print(auf.message)
    except Unauthorized as unauth:
        print(unauth.message)
else:
    print ("Error: Invalid authentication URL set.")

