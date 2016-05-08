#!/usr/bin/env python
# Boilerplate for preparing client objects
import os, sys

# v2 client
from keystoneclient.v2_0 import client as kclient
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

keystone = kclient.Client(**_keystone_creds)
neutron = nclient.Client(**_keystone_creds)
