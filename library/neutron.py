import requests, json, sys
#from neutronclient.v2_0 import client
#from credentials import get_credentials
from clients import neutron

def list_networks():
    networks = neutron.list_networks()
    return networks

def create_network(name,network_type="vxlan"):

    body_value = {
        "network": {
            "name": name,
            "admin_state_up": True,
            "provider:network_type": network_type
        }
    }

#    response = neutron.create_network(body=body_value)
#    return response["network"]["id"]
    return neutron.create_network(body=body_value)

def create_subnet(network_id,cidr):

    body_value = {
        "subnet": {
            "network_id": network_id,
            "cidr": cidr,
            "ip_version": "4",
            "enable_dhcp": False,
            "gateway_ip": None
        }
    }

    response = neutron.create_subnet(body=body_value)
    return response["subnet"]["id"]

def add_address_pair(port_id,ip_address,mac_address=None):

#    print port_id,ip_address,mac_address

    if mac_address is None:
        mac_address = get_macaddr_from_port(port_id)

    entry = {'ip_address':ip_address,'mac_address':mac_address}
    port_details = neutron.show_port(port_id)
    address_pairs = port_details["port"]["allowed_address_pairs"]

    address_pairs.append(dict(entry))

    req = {
        "port": {
            "allowed_address_pairs": address_pairs
        }
    }

    response = neutron.update_port(port_id, req)
#    return response["port"]["allowed_address_pairs"]

def create_port(network_id,hostname):

    port_name = hostname + "_" + network_id[:11]
    body_value = {
        "port": {
            "admin_state_up": True,
            "name": port_name,
            "network_id": network_id
         }
    }

    response = neutron.create_port(body=body_value)
    #print json.dumps(response, sort_keys=True, indent=4) // Debug Example

    return response["port"]["id"]


def get_fixedip_from_port(port_id):
    port_details = neutron.show_port(port_id)
    fixed_ip = port_details["port"]["fixed_ips"][0]["ip_address"]

    return fixed_ip

def get_macaddr_from_port(port_id):
    port_details = neutron.show_port(port_id)
    mac_addr = port_details["port"]["mac_address"]

    return mac_addr

def get_gateway_from_port(port_id):

    port_details = neutron.show_port(port_id)
    subnet_id = port_details["port"]["fixed_ips"][0]["subnet_id"]
    subnet_details = neutron.show_subnet(subnet_id)
    gateway_ip = subnet_details["subnet"]["gateway_ip"]
    subnet_mask = get_netmask_from_subnet(subnet_id)

    return gateway_ip,subnet_mask

def get_netmask_from_subnet(subnet_id):

    # Get address string and CIDR string from command line
    subnet_details = neutron.show_subnet(subnet_id)
    subnet_cidr = subnet_details["subnet"]["cidr"]
    (addrString, cidrString) = subnet_cidr.split('/')
    cidr = int(cidrString)

    # Initialize the netmask and calculate based on CIDR mask
    mask = [0, 0, 0, 0]
    for i in range(cidr):
	mask[i/8] = mask[i/8] + (1 << (7 - i % 8))

    # Print information, mapping integer lists to strings for easy printing
    subnet_mask = ".".join(map(str, mask))
#    print "Netmask:   " , ".".join(map(str, mask))
    return subnet_mask
