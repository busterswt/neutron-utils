import requests, json, sys
import argparse
from netaddr import *
from prettytable import PrettyTable
from library.clients import neutron

def build_float_table(args):

    # Get a list of external networks
    if args.network_id is not None:
	_params = {'id':network_id}
        networks = neutron.list_networks(**_params)
    if not args.allnetworks:
	_params = {'router:external':'True'}
        networks = neutron.list_networks(**_params)
    else:
        _params = {}
        networks = neutron.list_networks(**_params)

    # Using returned networks, build a table of subnets and floating info
    for network in networks['networks']:
        table = PrettyTable(["Tenant ID", "Network ID", "Network Name", "Subnet ID", "CIDR", "Usable", "Floating", "Other", "Remaining"])

	# Print network as the first line
	table.add_row([network['tenant_id'],network['id'],network['name'],"-","-","-","-","-","-"])

	# Check for subnets and list here. Count existing ports associated with the subnet.
	_params = {'network_id':network['id']}	
	subnets = neutron.list_subnets(**_params)
	for subnet in subnets['subnets']:
	    # Calculate total subnet size
	    cidr = IPNetwork(subnet['cidr'])
	    total_usable_ips = (cidr.size-2)

	    # Count total ports associated with subnet
	    _params = {'fixed_ips':'subnet_id=%s' % subnet['id']}
	    subnet_ports = neutron.list_ports(**_params)
	    total_subnet_ports = len(subnet_ports['ports'])

	    # Count total floating ip ports associated with subnet
	    _params = {'fixed_ips':'subnet_id=%s' % subnet['id'], 'device_owner':'network:floatingip'}
	    floating_ports = neutron.list_ports(**_params)
	    total_floating_ports = len(floating_ports['ports'])

	    # Calculate non-floating ports (DHCP, router, VM, etc.)
	    total_other_ports = (total_subnet_ports - total_floating_ports)
	    # Calculate remaining
	    total_remaining = total_usable_ips - total_subnet_ports	    
	    
            table.add_row(["-","-","-",subnet['id'],subnet['cidr'],total_usable_ips,total_floating_ports,total_other_ports,total_remaining])

	# Print the table
        print table

if __name__ == "__main__":
    # Build the floating tables
    # (todo) Allow user to specify network ID, tenant ID, or list all networks!

    parser = argparse.ArgumentParser(description='network.py - Utility to show IP address utilization')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--network-id', type=str, help='Provides IP address utilization for specified network', required=False, default=None)
    group.add_argument('--all', dest='allnetworks', action='store_true', help='Provides IP address utilization for all networks (default is external only)', required=False)
    parser.set_defaults(allnetworks=False)

    # Array for all arguments passed to script
    args = parser.parse_args()
    network_id = args.network_id

    # Build the table, passing the network_id (if provided)
    build_float_table(args)

