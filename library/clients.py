#!/usr/bin/env python
# Boilerplate for preparing client objects
import os, sys, logging
from urlparse import urlparse
from keystoneclient import session, exceptions
from keystoneclient.exceptions import AuthorizationFailure, Unauthorized

# v2 client
from keystoneclient.auth.identity import v2
from keystoneclient.v2_0 import client as k2client

# v3 client
from keystoneclient.auth.identity import v3
from keystoneclient.v3 import client as k3client

# Neutron client
from neutronclient.v2_0 import client as nclient

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
	auth = v2.Password(**_keystone_creds)
	sess = session.Session(auth=auth)
	keystone = k2client.Client(session=sess)
    except AuthorizationFailure as auf:
        print(auf.message)
    except Unauthorized as unauth:
        print(unauth.message)
elif "v3" in u.path:
    try:
	auth = v3.Password(**_keystone_creds)
	sess = session.Session(auth=auth)
	keystone = k3client.Client(session=sess)
    except AuthorizationFailure as auf:
        print(auf.message)
    except Unauthorized as unauth:
       	print(unauth.message)
else:
    print ("Error: Invalid authentication URL set!")


# Instantiate Neutron client
neutron = nclient.Client(**_keystone_creds)
