import requests, json, sys
from .clients import neutron

def get_segment_id_from_network(network_id):
    network_details = neutron.show_network(network_id)
    segmentation_id = network_details["network"]["provider:segmentation_id"]
    network_type = network_details["network"]["provider:network_type"]

    if network_type != "vlan":
        segmentation_id = "N/A"

    return segmentation_id

def get_fixedip_from_port(port_id):
    # Returns the (first) fixed IP of a port

    port_details = neutron.show_port(port_id)
    fixed_ip = port_details["port"]["fixed_ips"][0]["ip_address"]

    return fixed_ip

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

def get_ports_from_instance(instance_uuid):
    ports = neutron.list_ports(device_id=instance_uuid)
#    segmentation_id = network_details["network"]["provider:segmentation_id"]
#    network_type = network_details["network"]["provider:network_type"]

    return ports

def get_security_groups_from_port(port_uuid):
    port_details = neutron.show_port(port_uuid)
    port_security_groups = port_details["port"]["security_groups"]
#    security_groups = neutron.list_security_groups(port_uuid)
    return port_security_groups

def get_security_group_rules_from_group(rule_args):
    security_group_rules = neutron.list_security_group_rules(security_group_id=rule_args["security_group"],
                                                             direction=rule_args["direction"])

    return security_group_rules

def get_network_name(network_id):
    network_details = neutron.show_network(network_id)
    network_name = network_details["network"]["name"]
    return network_name


def get_network_l2(network_id):
    network_details = neutron.show_network(network_id)
    type = network_details["network"]["provider:network_type"]
    segmentation_id = network_details["network"]["provider:segmentation_id"]
    return type, segmentation_id
