#!/usr/bin/env python3
import ipaddress
import requests, json, sys
import argparse
import library.neutron as neutronlib
from colorama import Fore, Back, Style
from prettytable import PrettyTable
from library.clients import neutron

# Define some styles
BOLD = Style.BRIGHT
RST = Style.RESET_ALL
G = Fore.GREEN
R = Fore.RED
WonG = Back.GREEN + Fore.WHITE
WonR = Back.RED + Fore.WHITE

# Setup some defaults
s_allowed = WonG + "Allowed" + RST
s_notallowed = WonR + "Not Allowed" + RST
status = s_notallowed

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="secgrp.py - Utility to determine which security group allows certain traffic"
    )
    parser.add_argument(
        "--instance-uuid",
        type=str,
        help="Specify instance UUID",
        required=True,
        default=None,
    )
    parser.add_argument(
        "--src-ip",
        type=str,
        help="Specify source IP address (e.g. 173.44.5.29) or CIDR (e.g. 192.168.1.0/24). Defaults to 0.0.0.0/0 (any).",
        required=False,
        default="0.0.0.0/0",
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
        help="Specify destination port (e.g. None (any), 80, 443, 3306). Valid ports are 1:65536. Defaults to None (any).",
        required=False,
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

    instance_ports = neutronlib.get_ports_from_instance(args.instance_uuid)
    instance_security_groups = []
    for instance_port in instance_ports["ports"]:
        instance_security_groups = neutronlib.get_security_groups_from_port(instance_port["id"])

    instance_security_group_rules = []
    for instance_security_group in instance_security_groups:
        rule_args = {'security_group': instance_security_group,
                     'direction': args.direction,
                     'dst_port': args.dst_port}
        instance_security_group_rules = neutronlib.get_security_group_rules_from_group(rule_args)["security_group_rules"]

    # Build the security group rule table:
    table = PrettyTable(
        [
            "Security Group ID",
            "Security Group Rule ID",
            "Remote IP Prefix",
            "Protocol",
            "Port Range",
            "Source IP Allowed?",
            "Protocol Allowed?",
            "Dest Port Allowed?",
        ]
    )

    for rule in instance_security_group_rules:
        src_ip_allowed = False
        dst_port_allowed = False
        proto_allowed = False

        remote_ip_prefix = rule["remote_ip_prefix"]

        if remote_ip_prefix is not None:
            n1 = ipaddress.ip_network(args.src_ip)
            n2 = ipaddress.ip_network(remote_ip_prefix)

        # Test to see if the source ip overlaps the remote_ip_prefix
        if(n1.overlaps(n2)):
            src_ip_allowed = True

        # Test to see if the protocol is allowed
        if rule["protocol"] is None:
            proto_allowed = True
        elif args.protocol is None:
            proto_allowed = True
        else:
            if args.protocol in rule["protocol"]:
                proto_allowed = True

        # Test to see if the dst_port is allowed
        if(rule["port_range_min"] and rule["port_range_max"]) is None:
            dst_port_allowed = True
        elif(args.dst_port is not None):
           if(rule["port_range_min"] <= int(args.dst_port) <= rule["port_range_max"]):
               dst_port_allowed = True

        # Check to see if this rule is a match across the board
        if(src_ip_allowed and proto_allowed and dst_port_allowed):
            status = s_allowed
            COLOR = BOLD + G
        else:
            COLOR = RST

        table.add_row([COLOR + rule["security_group_id"] + RST,
                      COLOR + rule["id"] + RST,
                      COLOR + rule["remote_ip_prefix"] + RST,
                      COLOR + str(rule["protocol"]).replace('None','any') + RST,
                      COLOR + "%s:%s" % (str(rule["port_range_min"]).replace('None','any'),
                                 str(rule["port_range_max"]).replace('None','any')) + RST,
                      COLOR + str(src_ip_allowed) + RST,
                      COLOR + str(proto_allowed) + RST,
                      COLOR + str(dst_port_allowed) + RST,
                      ])

    table.title = ("Instance: %s | "
                   "Source IP: %s | "
                   "Protocol: %s | "
                   "Destination Port: %s | "
                   "Direction: %s | "
                   "Status: %s " % (BOLD + args.instance_uuid + RST,
                                      BOLD + args.src_ip + RST,
                                      BOLD + str(args.protocol).replace('None','any') + RST,
                                      BOLD + str(args.dst_port).replace('None','any') + RST,
                                      BOLD + args.direction + RST,
                                      BOLD + status + RST)
                  )

    print(table)
