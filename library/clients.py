#!/usr/bin/env python
# Boilerplate for preparing client objects
import os, sys

# v2 client
from keystoneclient.v2_0 import client as kclient
from neutronclient.v2_0 import client as nclient
from novaclient import client as novaclient
from keystoneauth1 import loading
from keystoneauth1 import session

_keystone_creds = {}
try:
    _keystone_creds['username'] = os.environ['OS_USERNAME']
    _keystone_creds['password'] = os.environ['OS_PASSWORD']
    _keystone_creds['auth_url'] = os.environ['OS_AUTH_URL']
    _keystone_creds['tenant_name'] = os.environ['OS_TENANT_NAME']
except KeyError, e:
    print ("Openstack environment variable %s is not set!") % e
    sys.exit(1)

_nova_creds = {}
_nova_creds['username'] = os.environ['OS_USERNAME']
_nova_creds['password'] = os.environ['OS_PASSWORD']
_nova_creds['auth_url'] = os.environ['OS_AUTH_URL']
#_nova_creds['tenant_name'] = os.environ['OS_TENANT_NAME']
_nova_creds['project_id'] = os.environ['OS_PROJECT_ID']

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(**_nova_creds)
sess = session.Session(auth=auth)

keystone = kclient.Client(**_keystone_creds)
nova = novaclient.Client(2,session=sess)
neutron = nclient.Client(**_keystone_creds)
