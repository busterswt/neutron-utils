import requests, json, sys
import argparse
from prettytable import PrettyTable
from library.clients import neutron

def get_network_name(network_id):
    network_details = neutron.show_network(network_id)
    network_name = network_details["network"]["name"]
    return network_name

def get_network_l2(network_id):
    network_details = neutron.show_network(network_id)
    type = network_details["network"]["provider:network_type"]
    segmentation_id = network_details["network"]["provider:segmentation_id"]
    return type,segmentation_id

def build_router_table(router_id):

    # Get a list of routers (by ID or all)
    if router_id is not None:
        _params = {'id':router_id}
        routers = neutron.list_routers(**_params)
    else:
        routers = neutron.list_routers()

    ## Print Routers:
    for router in routers['routers']:
        table = PrettyTable(["Tenant ID", "Router ID", "Router Name", "Network Name", "External", "Type", "Segmentation ID",  "Network ID"])

	# Print router as the first line
	table.add_row([router['tenant_id'],router['id'],router['name'],"-","-","-","-","-"])

	# Check for external network and list here
	router_gateway_ports = neutron.list_ports(device_id=router['id'],device_owner="network:router_gateway")
	for port in router_gateway_ports['ports']:
	    type,segmentation_id = get_network_l2(port['network_id'])
            table.add_row(["-","-","-",get_network_name(port['network_id']),"***",type,segmentation_id,port['network_id']])

	# Print internal networks 
	router_interface_ports = neutron.list_ports(device_id=router['id'],device_owner="network:router_interface")
        for port in router_interface_ports['ports']:
	    type,segmentation_id = get_network_l2(port['network_id'])
	    table.add_row(["-","-","-",get_network_name(port['network_id']),"-",type,segmentation_id,port['network_id']])

	# Print the table
        print table


if __name__ == "__main__":
    # Build the router tables

    parser = argparse.ArgumentParser(description='router.py - Utility to show routers and connected networks')
    parser.add_argument('--router-id', type=str, help='Router UUID', required=False, default=None)

    # Array for all arguments passed to script
    args = parser.parse_args()
    router_id = args.router_id

    # Build the table, passing the router_id (if provided)
    build_router_table(router_id)
