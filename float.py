import requests, json, sys
import argparse, string
from netaddr import *
from prettytable import PrettyTable
from library.clients import neutron
from library.clients import nova

def get_network_name(network_id):
    network_details = neutron.show_network(network_id)
    network_name = network_details["network"]["name"]
    return network_name

def get_network_id(port_id):

    if port_id is not None:
        port = neutron.show_port(port_id)
        return port['port']['network_id']
    else: 
	return 'N/A'

def get_instance_info_from_port(port_id):

    if port_id is not None:
        port = neutron.show_port(port_id)

    try:
        instance = nova.servers.get(port['port']['device_id'])
	return instance.id,instance.name
    except:
        # Unable to get instance info from Nova. May not be an instance port
        return 'N/A','N/A'

def get_agent(router_id):
    # (todo) make compatible with HA routers
    _params = {'router':router_id}
    agents = neutron.list_l3_agent_hosting_routers(**_params)
    for agent in agents['agents']:
        return agent['host']

def build_float_table(args):

    # Get a list of external networks
    if args.floating_ip is not None:
	_params = {'floating_ip_address':args.floating_ip}
        floatingips = neutron.list_floatingips(**_params)
    elif args.network_id is not None:
        _params = {'floating_network_id':args.network_id}
        floatingips = neutron.list_floatingips(**_params)
    elif args.fixed_ip is not None:
        _params = {'fixed_ip_address':args.fixed_ip}
        floatingips = neutron.list_floatingips(**_params)
    elif args.tenant_id is not None:
        _params = {'tenant_id':args.tenant_id}
        floatingips = neutron.list_floatingips(**_params)

    # Using returned networks, build a table of subnets and floating info
    table = PrettyTable(["tenant_id","floating_network_name", "floating_ip_address", "fixed_ip_address", "fixed_network_id", "router_id", "agent_name", "instance_id"])
    for floatingip in floatingips['floatingips']:

	instanceid = None
	instancename = None
	agent_name = None

	if floatingip['port_id'] is not None:
	    instanceid,instancename = get_instance_info_from_port(floatingip['port_id'])	    

        # Get agent name
	if floatingip['router_id'] is not None:
            agent_name = get_agent(floatingip['router_id'])

	# Print network as the first line
	table.add_row([floatingip['tenant_id'],get_network_name(floatingip['floating_network_id']),
			floatingip['floating_ip_address'],floatingip['fixed_ip_address'],get_network_id(floatingip['port_id']),
			floatingip['router_id'],agent_name,instanceid])


    # Print the table (Limit columns returned)
    if args.fields is not None:
	fields = args.fields.split(",")
	try:
      	    table = table.get_string(fields=fields)
	except Exception,e:
	    print "Unable to filter results. %s. Continuing to print the table." % e
    print table

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='float.py - Utility to identify information related to floating IPs')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--floating-ip', dest='floating_ip', type=str, help='Provides information related to provided floating IP', required=False, default=None)
    group.add_argument('--network-id', dest='network_id', type=str, help='Provides floating IPs related to provided floating network ID', required=False, default=None)
    group.add_argument('--fixed-ip', dest='fixed_ip', type=str, help='Provides floating IPs related to provided fixed ID (Warning: May return multiple matches)', required=False, default=None)
    group.add_argument('--tenant-id', dest='tenant_id', type=str, help='Provides floating IPs related to provided tenant ID', required=False, default=None)
    parser.add_argument('-f', dest='fields', type=str, help='Limit output to specified fields using comma separated list', required=False, default=None)
    parser.add_argument('-s', dest='sort', type=str, help='Sort by specified field', required=False, default=None)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Build the table, passing the network_id (if provided)
    build_float_table(args)

