#!/usr/bin/env python
# Boilerplate for preparing client objects
import os, sys

#from keystoneclient import session as ksession
from keystoneauth1 import session as ksession
from keystoneclient.auth.identity import v3
from keystoneclient.v3 import client as kclient
from neutronclient.v2_0 import client as nclient
from novaclient import client as novaclient

_keystone_creds = {}
try:
    _keystone_creds['username'] = os.environ['OS_USERNAME']
    _keystone_creds['password'] = os.environ['OS_PASSWORD']
    _keystone_creds['auth_url'] = os.environ['OS_AUTH_URL']
    _keystone_creds['project_name'] = os.environ['OS_PROJECT_NAME']
#    _keystone_creds['tenant_name'] = os.environ['OS_TENANT_NAME']
#    _keystone_creds['project_id'] = os.environ['OS_PROJECT_ID']
    _keystone_creds['user_domain_name'] = os.environ['OS_USER_DOMAIN_NAME']
    _keystone_creds['project_domain_name'] = os.environ['OS_PROJECT_DOMAIN_NAME']
except KeyError as e:
    print("Openstack environment variable %s is not set!" % e)
    sys.exit(1)

auth = v3.Password(**_keystone_creds)
sess = ksession.Session(auth=auth,verify=False)

keystone = kclient.Client(session=sess,insecure=True)
neutron = nclient.Client(session=sess,insecure=True)
nova = novaclient.Client("2.9", session=sess,insecure=True)

