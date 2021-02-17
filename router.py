#!/usr/bin/env python3
import requests, json, sys
import argparse
from prettytable import PrettyTable
from library.clients import neutron
from colorama import Fore, Back, Style

# Define some styles
BOLD = Style.BRIGHT
RST = Style.RESET_ALL
G = Fore.GREEN
R = Fore.RED
WonG = Back.GREEN + Fore.WHITE
WonR = Back.RED + Fore.WHITE

def get_network_name(network_id):
    network_details = neutron.show_network(network_id)
    network_name = network_details["network"]["name"]
    return network_name


def get_network_l2(network_id):
    network_details = neutron.show_network(network_id)
    type = network_details["network"]["provider:network_type"]
    segmentation_id = network_details["network"]["provider:segmentation_id"]
    return type, segmentation_id


def build_router_table(args):

    # Get a list of routers (by ID or all)
    if args.router_id is not None:
        _params = {"id": args.router_id}
        routers = neutron.list_routers(**_params)
        generic_router_table(routers)
    elif args.project_id is not None:
        _params = {"project_id": args.project_id}
        routers = neutron.list_routers(**_params)
        generic_router_table(routers)
    elif args.network_id is not None:
        router_ids = get_routers_by_network(args.network_id)
        _params = {"id": router_ids}
        routers = neutron.list_routers(**_params)
        generic_router_table(routers)
    else:
        routers = neutron.list_routers()
        generic_router_table(routers)


def get_routers_by_network(network_id):
    # Return a list of routers connected to the provided network

    # Get external ports
    external_ports = neutron.list_ports(
        network_id=network_id, device_owner="network:router_gateway"
    )
    # Get internal ports
    internal_ports = neutron.list_ports(
        network_id=network_id, device_owner="network:router_interface"
    )

    # Combine the list and return all matching router IDs (should be unique?)
    router_ports = external_ports["ports"] + internal_ports["ports"]
    router_ids = []
    for port in router_ports:
        router_ids.append(port["device_id"])
    return router_ids


def generic_router_table(routers):

    for router in routers["routers"]:

        # Print Routers:
        table = PrettyTable(
            [
                "Network Name",
                "Ext",
                "Type",
                "Segment ID",
                "Network ID",
            ]
        )

        # Check for external network and list here
        router_gateway_ports = neutron.list_ports(
            device_id=router["id"], device_owner="network:router_gateway"
        )
        for port in router_gateway_ports["ports"]:
            type, segmentation_id = get_network_l2(port["network_id"])
            table.add_row(
                [
                    get_network_name(port["network_id"]),
                    "***",
                    type,
                    segmentation_id,
                    port["network_id"],
                ]
            )

        # Print internal networks
        router_interface_ports = neutron.list_ports(
            device_id=router["id"], device_owner="network:router_interface"
        )
        for port in router_interface_ports["ports"]:
            type, segmentation_id = get_network_l2(port["network_id"])
            table.add_row(
                [
                    get_network_name(port["network_id"]),
                    "",
                    type,
                    segmentation_id,
                    port["network_id"],
                ]
            )

        table.title = ("Router ID: %s | "
                       "Router Name:: %s | "
                       "Project ID: %s" % (BOLD + router["id"] + RST,
                                           BOLD + router["name"] + RST,
                                           BOLD + router["project_id"] + RST)
                      )
        print(table)


if __name__ == "__main__":
    # Build the router tables

    parser = argparse.ArgumentParser(
        description="router.py - Utility to show routers and connected networks"
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--router-id",
        type=str,
        help="Provides details for specified router",
        required=False,
        default=None,
    )
    group.add_argument(
        "--project-id",
        type=str,
        help="Provides details of routers associated with specified project",
        required=False,
        default=None,
    )
    group.add_argument(
        "--network-id",
        type=str,
        help="Provides details of routers connected to specified network",
        required=False,
        default=None,
    )

    # Array for all arguments passed to script
    args = parser.parse_args()
    # Build the table, passing the router_id (if provided)
    build_router_table(args)
