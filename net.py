import requests, json, sys
from pprint import pprint
#from neutronclient.v2_0 import client
from prettytable import PrettyTable
import library.neutron as neutronlib
import library.config as configlib
import library.nova as novalib
import library.keystone as keystonelib
from library.clients import neutron

#networks = neutron.list_networks()
#routers = neutron.list_routers()

#print "Networks:"
#for network in networks['networks']:
#    print (network['id'])

#print "Routers:"
#print routers

def get_network_name(network_id):
    network_details = neutron.show_network(network_id)
    network_name = network_details["network"]["name"]
    return network_name

def build_router_table():
    routers = neutron.list_routers()

    ## Print Routers:
    print "Router details:"
    for router in routers['routers']:
        details = PrettyTable(["Tenant ID", "Router ID", "Router Name", "Network Name", "External", "Network ID"])
	details.align["Tenant ID"] = "l" # right align

	# (todo) Check for external network and list here
	details.add_row([router['tenant_id'],router['id'],router['name'],get_network_name(router['external_gateway_info']['network_id']),"***",router['external_gateway_info']['network_id']])

	# (todo) print internal networks - Somehow get router port list?
	router_ports = neutron.list_ports(device_id=router['id'],device_owner="network:router_interface")
        for port in router_ports['ports']:
	    details.add_row(["","","",get_network_name(port['network_id']),"",port['network_id']])

	# Print the table
        print details


# Build the router tables
# (todo) Allow user to specify router ID, tenant ID, or list all routers!
build_router_table()
