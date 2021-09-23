#!/usr/bin/env python3
import ipaddress
import requests, json, sys, os
import argparse
import library.neutron as neutronlib
from library.clients import neutron
from termcolor import colored, cprint
from beautifultable import BeautifulTable

# References:
# https://beautifultable.readthedocs.io/en/latest/quickstart.html
# https://beautifultable.readthedocs.io/en/latest/source/beautifultable.html#beautifultable.BTColumnCollection.padding

# disable tracebacks
if(os.environ.get('DEBUG')=='1'):
    sys.tracebacklimit = 1
else:
    sys.tracebacklimit = 0

########################################
##### Begin Functions
########################################

def check_port(dst_port,port_range_min,port_range_max):
# Test to see if the dst_port is allowed

    if not (0 <= int(dst_port) <= 65535):
        raise Exception("Sorry, destination port range must be between 0 and 65535!")

    if(port_range_min and port_range_max) is None:
        return True
    elif(dst_port is not None):
       if(port_range_min <= int(args.dst_port) <= port_range_max):
           return True


# There are two (mutually exclusive) checks involved:
# 1. Source IP Match - or -
# 2. Source Group (membership) match
def check_source_grp(rule, src_vm):

    if(rule["remote_group_id"] is not None):
        # Test to see if security groups for source VM match allowed remote groups
        src_security_groups = neutronlib.get_security_groups_from_instance(src_vm)

        # compare src vs dst
        if(rule["remote_group_id"] in src_security_groups):
            return True

def check_source_ip(rule, src_ip):
# Disable strict to workaround misconfigured sec grp rules

    # Source IP can be a fixed, floating, or external IP
    # Test to see if the source ip (n1) overlaps the remote_ip_prefix (n2)
    remote_ip_prefix = rule["remote_ip_prefix"]
    if remote_ip_prefix is None:
        n1 = ipaddress.ip_network(src_ip)
        n2 = ipaddress.ip_network('0.0.0.0/0')
    elif remote_ip_prefix is not None:
        n1 = ipaddress.ip_network(src_ip)
        try:
            n2 = ipaddress.ip_network(remote_ip_prefix)
            if(n1.overlaps(n2)):
                return True
        except:
            cprint("\nERROR: Invalid remote_ip_prefix %s for rule %s in security group %s. Skipping!" % (rule["remote_ip_prefix"],rule["id"],rule["security_group_id"]), 'yellow')

#    if(n1.overlaps(n2)):
#        return True


def check_protocol(rule, protocol):
# Test to see if the protocol is allowed

    if rule["protocol"] is None:
        return True
    elif args.protocol is None:
        return True
    else:
        if args.protocol in rule["protocol"]:
            return True

########################################
##### End Functions
########################################

if __name__ == "__main__":
########################################
##### Begin Args
########################################

    parser = argparse.ArgumentParser(
        description="secgrp.py - Utility to determine which security group (and rule) allows specified traffic."
                    " Requires access to OpenStack API."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument(
        "--insecure",
        type=bool,
        help="Validate SSL",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--instance-id",
        type=str,
        help="Specify (destination) instance UUID",
        required=True,
        default=None,
    )
    group.add_argument(
        "--src-vm",
        type=str,
        help="Specify source instance UUID. Compares security groups for source VM against allowed remote groups for destination VM.",
        required=False,
        default=None,
    )
    group.add_argument(
        "--src-ip",
        type=str,
        help="Specify source IP address (e.g. 173.44.5.29) or CIDR (e.g. 192.168.1.0/24). Defaults to None (any).",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--protocol",
        type=str,
        help="Specify protocol (e.g. None (any), tcp, udp, icmp). Defaults to None (any).",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--dst-port",
        type=str,
        help="Specify destination port (e.g. None (any), 80, 443, 3306). Valid ports are 1:65536.",
        required=True,
        default=None,
    )
    parser.add_argument(
        "--direction",
        type=str,
        help="Specify direction (e.g. ingress, egress). Defaults to ingress.",
        required=False,
        default="ingress",
    )

    # Array for all arguments passed to script
    args = parser.parse_args()

########################################
##### End Args
########################################

########################################
##### Begin Defaults
########################################

    status = colored("Not Allowed", 'red', attrs=['bold'])

########################################
##### End Defaults
########################################

    cprint("\nneutron-utils: secgrp -- security group rule checker\n")

    # Build the beautiful table
    table = BeautifulTable(maxwidth=180)
    table.columns.header = [
            "",
            "Security Group ID",
            "Security Group Rule ID",
            "Rule\nType",
            "Allowed\nRemote IP",
            "Allowed\nRemote Group",
            "Protocol",
            "Port Range"
        ]

    # Check to see if we specified src_ip or src_vm
    if(args.src_ip is not None):
        ruletype = "IP"
        source = args.src_ip
    elif(args.src_vm is not None):
        ruletype = "Group"
        source = args.src_vm

    # Get all Neutron ports for given instance
    instance_ports = neutronlib.get_ports_from_instance(args.instance_id)

    # Get all security groups for all ports of given instance
    instance_security_groups = neutronlib.get_security_groups_from_instance(args.instance_id)

    if(os.environ.get('DEBUG')=='1'):
        print(instance_security_groups)

    instance_security_group_rules = []
    for instance_security_group in instance_security_groups:
        rule_args = {'security_group': instance_security_group,
                     'direction': args.direction,
                     'dst_port': args.dst_port}
        instance_security_group_rules += neutronlib.get_security_group_rules_from_group(rule_args)["security_group_rules"]

    # Iterate through all of the rules for the destination VM
    row_id = 1
    for rule in instance_security_group_rules:
        if(os.environ.get('DEBUG')=='1'):
            print(rule)

        # Setup some defaults
        src_ip_allowed = False
        dst_port_allowed = False
        proto_allowed = False

        # Define rule type as 'IP' where remote group is None
        if rule["remote_group_id"] is None:
            r_ruletype = "IP"
            if(ruletype == r_ruletype):
                s_ruletype = colored("IP", attrs=['bold'])
            else:
                s_ruletype = "IP (N/A)"
        else:
        # Otherwise, define rule type as 'GROUP' when remote group is not None
            r_ruletype = "Group"
            if(ruletype == r_ruletype):
                s_ruletype = colored("Group", attrs=['bold'])
            else:
                s_ruletype = "Group (N/A)"

        # Check to see if we specified src_ip or src_vm
        # Highlight the rule only if it matches our type (ip vs src)
        if(args.src_ip is not None and r_ruletype == "IP"):
            remote = str(rule["remote_ip_prefix"])
            if check_source_ip(rule, args.src_ip):
                src_ip_allowed = True
                s_remote_ip = colored(str(rule["remote_ip_prefix"]).replace('None','any'), 'green', attrs=['bold'])
                s_remote_grp = colored(str(rule["remote_group_id"]))
            else:
                s_remote_ip = colored(str(rule["remote_ip_prefix"]).replace('None','any'), 'red', attrs=['bold'])
                s_remote_grp = colored(str(rule["remote_group_id"]))
        elif(args.src_vm is not None and r_ruletype == "Group"):
            remote = str(rule["remote_group_id"])
            if check_source_grp(rule, args.src_vm):
                src_ip_allowed = True
                s_remote_ip = colored(str(rule["remote_ip_prefix"]).replace('None','any'))
                s_remote_grp = colored(str(rule["remote_group_id"]), 'green', attrs=['bold'])
            else:
                s_remote_ip = colored(str(rule["remote_ip_prefix"]).replace('None','any'))
                s_remote_grp = colored(str(rule["remote_group_id"]), 'red', attrs=['bold'])
        else:
            s_remote_ip = str(rule["remote_ip_prefix"])
            s_remote_grp = str(rule["remote_group_id"])

        # Check if protocol is allowed
        if((args.src_ip is not None and r_ruletype == "IP") or
           (args.src_vm is not None and r_ruletype == "Group")):
            if check_protocol(rule, args.protocol):
                proto_allowed = True
                s_proto = colored(rule["protocol"], 'green', attrs=['bold'])
            else:
                s_proto = colored(rule["protocol"], 'red', attrs=['bold'])
        else:
             s_proto = rule["protocol"]

        # Check if dst port is allowed
        if((args.src_ip is not None and r_ruletype == "IP") or
           (args.src_vm is not None and r_ruletype == "Group")):
            if check_port(args.dst_port,rule["port_range_min"],rule["port_range_max"]):
               dst_port_allowed = True
               s_dstport = colored("%s:%s" % (
                                     str(rule["port_range_min"]).replace('None','any'),
                                     str(rule["port_range_max"]).replace('None','any')),
                                         'green', attrs=['bold'])
            else:
               s_dstport = colored("%s:%s" % (
                                     str(rule["port_range_min"]).replace('None','any'),
                                     str(rule["port_range_max"]).replace('None','any')),
                                         'red', attrs=['bold'])
        else:
            s_dstport = "%s:%s" % (str(rule["port_range_min"]).replace('None','any'),
                                   str(rule["port_range_max"]).replace('None','any'))

        # Check to see if this rule is a match across the board. If so, highlight it.
        if(os.environ.get('DEBUG')=='1'):
            print("Src: %s Proto: %s Port: %s" % (src_ip_allowed,proto_allowed,dst_port_allowed))

        if(src_ip_allowed and proto_allowed and dst_port_allowed):
            status = colored("Allowed", 'green', attrs=['bold'])
            s_groupid = colored(rule["security_group_id"], 'green', attrs=['bold', 'reverse'])
            s_ruleid = colored(rule["id"], 'green', attrs=['bold', 'reverse'])
            if(args.src_ip is not None):
                s_remote_ip = colored(str(rule["remote_ip_prefix"]).replace('None','any'), 'green', attrs=['bold', 'reverse'])
                s_remote_grp = str(rule["remote_group_id"])
            elif(args.src_vm is not None):
                s_remote_ip = str(rule["remote_ip_prefix"]).replace('None','any')
                s_remote_grp = colored(str(rule["remote_group_id"]), 'green', attrs=['bold', 'reverse'])
            s_proto = colored(rule["protocol"], 'green', attrs=['bold', 'reverse'])
            s_dstport = colored("%s:%s" % (
                                 str(rule["port_range_min"]).replace('None','any'),
                                 str(rule["port_range_max"]).replace('None','any')),
                                     'green', attrs=['bold', 'reverse'])
        else:
            s_groupid = rule["security_group_id"]
            s_ruleid = rule["id"]

        table.rows.append([
                      row_id,
                      s_groupid,
                      s_ruleid,
                      s_ruletype,
                      s_remote_ip,
                      s_remote_grp,
                      s_proto,
                      s_dstport,
                      ])
        row_id += 1

    # Build a short header for the table
    cprint("Destination (VM): %s" % str(args.instance_id))
    cprint("Source (IP or VM): %s" % source)
    cprint("Protocol: %s" % str(args.protocol).replace('None','any'))
    cprint("Destination Port: %s" % str(args.dst_port).replace('None','any'))
    cprint("Direction: %s" % str(args.direction))
    cprint("Status: %s\n" % status)
    cprint("Highlighted rules signify match based on: Source %s\n" % ruletype)

    print(table)
    cprint("\n")
