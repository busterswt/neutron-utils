# neutron-utils

A collection of utilities to make Neutron better.

## Installing

1. Clone the repo:

`git clone https://github.com/busterswt/neutron-utils/ ~/neutron-utils`

2. Build a venv:

```
mkdir ~/venvs
python3 -m venv ~/venvs/neutron-utils
```

3. Install dependencies within the venv:

```
source ~/venvs/neutron-utils/bin/activate
python3 -m pip install -r requirements.txt
```

## router.py

```
usage: router.py [-h]
                 [--router-id ROUTER_ID | --project-id PROJECT_ID | --network-id NETWORK_ID]

router.py - Utility to show routers and connected networks

optional arguments:
  -h, --help            show this help message and exit
  --router-id ROUTER_ID
                        Provides details for specified router
  --project-id PROJECT_ID
                        Provides details of routers associated with specified
                        tenant
  --network-id NETWORK_ID
                        Provides details of routers connected to specified
                        network
```

### Example

```
(neutron-utils) 🌕OpenStack Lab % ./router.py --router 5158265b-830a-4609-afd2-1f4911fc752c
+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|          Router ID: 5158265b-830a-4609-afd2-1f4911fc752c | Router Name: kubernetes-the-hard-way-router | Project ID: d0af694edc8f4d28babe4c0060f5764e           |
+----------------------------------------------+--------+------------+---------------------+-----------------------------------------------------------------------+
|                 Network Name                 |  Ext   |    Type    |      Segment ID     |                               Network ID                              |
+----------------------------------------------+--------+------------+---------------------+-----------------------------------------------------------------------+
|                     LAN                      |  ***   |    vlan    |         102         |                  d0084ac0-f70e-4f01-b4bb-d82429fa095e                 |
|           kubernetes-the-hard-way            |        |   vxlan    |          59         |                  cb177250-15d6-426f-8fb2-38e65aa30add                 |
+----------------------------------------------+--------+------------+---------------------+-----------------------------------------------------------------------+
```

## network.py

```
usage: network.py [-h] [--network-id NETWORK_ID | --all]

network.py - Utility to show IP address utilization

optional arguments:
  -h, --help            show this help message and exit
  --network-id NETWORK_ID
                        Provides IP address utilization for specified network
  --all                 Provides IP address utilization for all networks
                        (default is external only)
```

### Example

```
(neutron-utils) 🌕OpenStack Lab % ./network.py --network-id 0e4fa560-1483-4ac5-be44-0542503f1e5a
+--------------------------------------------------------------------------------------------------------------------------------------------------------+
|            Network ID: 0e4fa560-1483-4ac5-be44-0542503f1e5a | Project ID: 7a8df96a3c6a47118e60e57aa9ecff54 | Network Name: rpn_multisegment            |
+----------------------------------------------------------------+-------------------------+-------------+----------------+-----------+------------------+
|                           Subnet ID                            |           CIDR          |    Usable   |    Floating    |   Other   |    Remaining     |
+----------------------------------------------------------------+-------------------------+-------------+----------------+-----------+------------------+
|              0ce6d93d-87a3-4f20-88d1-fd100e2b2fad              |      10.206.0.0/24      |     254     |       0        |     3     |       251        |
|              a2009c72-b0e3-4bf3-b286-97c59d13800a              |      10.106.0.0/24      |     254     |       0        |     1     |       253        |
+----------------------------------------------------------------+-------------------------+-------------+----------------+-----------+------------------+
```

## float.py

```
usage: float.py [-h]
                (--floatingip FLOATINGIP | --network-id NETWORK_ID | --fixedip FIXEDIP | --project-id PROJECT_ID)

float.py - Utility to identify information related to floating IPs

optional arguments:
  -h, --help            show this help message and exit
  --floatingip FLOATINGIP
                        Provides information related to provided floating IP
  --network-id NETWORK_ID
                        Provides floating IPs related to provided floating
                        network ID
  --fixedip FIXEDIP     Provides floating IPs related to provided fixed ID.
                        (Warning: May return multiple matches)
  --project-id PROJECT_ID
                        Provides floating IPs related to provided project ID.
```

### Example

```
(neutron-utils) 🌕OpenStack Lab % ./float.py --network-id d0084ac0-f70e-4f01-b4bb-d82429fa095e
+----------------------------------+------------------+---------------+-----------------+--------------------------------------+--------------------------------------+-------------+--------------------------------------+
|            Project ID            | Floating Network |  Floating IP  |     Fixed IP    |            Fixed Network             |              Router ID               |  Agent Name |             Instance ID              |
+----------------------------------+------------------+---------------+-----------------+--------------------------------------+--------------------------------------+-------------+--------------------------------------+
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.230 | 192.168.188.153 | 3dabe4e9-354e-42ad-bba5-fcd3c61b13f3 | 03cc8432-c2f4-4d20-b35c-4a015f8959e6 | lab-infra01 |                 N/A                  |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.206 |   10.240.0.245  | cb177250-15d6-426f-8fb2-38e65aa30add | 5158265b-830a-4609-afd2-1f4911fc752c | lab-infra01 | a427dc10-370b-4e56-952a-ff0ce47a5b86 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.211 |   10.240.0.186  | cb177250-15d6-426f-8fb2-38e65aa30add | 5158265b-830a-4609-afd2-1f4911fc752c | lab-infra01 | 7e33188b-6721-4ecb-9d2c-1869b47cef6c |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.219 |   10.240.0.254  | cb177250-15d6-426f-8fb2-38e65aa30add | 5158265b-830a-4609-afd2-1f4911fc752c | lab-infra01 | 1bf14433-1e92-48fa-aeb0-a59de608de26 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.166 |   10.240.0.171  | cb177250-15d6-426f-8fb2-38e65aa30add | 5158265b-830a-4609-afd2-1f4911fc752c | lab-infra01 |                 N/A                  |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.205 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.227 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.202 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.234 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.216 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.236 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 8b29250a1f374021bf4b0812b583be90 |       LAN        | 192.168.2.222 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.217 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.218 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.207 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.204 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.238 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.229 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.201 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.212 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.203 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.226 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.210 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| 7a8df96a3c6a47118e60e57aa9ecff54 |       LAN        | 192.168.2.228 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
| d0af694edc8f4d28babe4c0060f5764e |       LAN        | 192.168.2.239 |       None      |                 N/A                  |                 None                 |     None    |                 None                 |
+----------------------------------+------------------+---------------+-----------------+--------------------------------------+--------------------------------------+-------------+--------------------------------------+
```

:warning: The float.py script may take a while to run depending on the size of the network.

## secgrp.py

```
usage: secgrp.py [-h]
              --instance-uuid INSTANCE_UUID [--src-ip SRC_IP] [--protocol PROTOCOL] [--dst-port DST_PORT] [--direction DIRECTION]

secgrp.py - Utility to determine which security group allows certain traffic

optional arguments:
  -h, --help            show this help message and exit
  --instance-uuid INSTANCE_UUID
                        Specify instance UUID
  --src-ip SRC_IP       Specify source IP address (e.g. 173.44.5.29) or CIDR (e.g. 192.168.1.0/24). Defaults to 0.0.0.0/0 (any).
  --protocol PROTOCOL   Specify protocol (e.g. None (any), tcp, udp, icmp). Defaults to None (any).
  --dst-port DST_PORT   Specify destination port (e.g. None (any), 80, 443, 3306). Valid ports are 1:65536. Defaults to None (any).
  --direction DIRECTION
                        Specify direction (e.g. ingress, egress). Defaults to ingress.
```

### Example

```
(neutron-utils) 🌕OpenStack Lab % ./secgrp.py --instance-uuid 93fd49ec-3113-4fa2-96f5-d16418da420f --dst-port 80
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                    Instance: 93fd49ec-3113-4fa2-96f5-d16418da420f | Source IP: 0.0.0.0/0 | Protocol: any | Destination Port: 80 | Direction: ingress | Status: Allowed                                    |
+----------------------------------------------+----------------------------------------------+----------------------+------------+---------------+------------------------+-----------------------+------------------------+
|              Security Group ID               |            Security Group Rule ID            |   Remote IP Prefix   |  Protocol  |   Port Range  |   Source IP Allowed?   |   Protocol Allowed?   |   Dest Port Allowed?   |
+----------------------------------------------+----------------------------------------------+----------------------+------------+---------------+------------------------+-----------------------+------------------------+
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     030cf802-622b-43af-a354-a42a1019760a     |      0.0.0.0/0       |    tcp     |    any:any    |          True          |          True         |          True          |
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     318584e3-b4f2-4cf9-9c22-8299a617586c     |      0.0.0.0/0       |    udp     |    any:any    |          True          |          True         |          True          |
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     531362cc-1e9d-46cc-8640-4db612d4606d     |      5.5.5.0/24      |    tcp     |     80:80     |          True          |          True         |          True          |
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     5512f55b-be90-4bfd-9ae2-0e9aa48acf3a     |      0.0.0.0/0       |    icmp    |    any:any    |          True          |          True         |          True          |
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     e07234d6-eb6e-4b31-909f-84aaca97ab7c     |      0.0.0.0/0       |    tcp     |     80:80     |          True          |          True         |          True          |
+----------------------------------------------+----------------------------------------------+----------------------+------------+---------------+------------------------+-----------------------+------------------------+

(neutron-utils) 🌕OpenStack Lab % ./secgrp.py --instance-uuid 93fd49ec-3113-4fa2-96f5-d16418da420f --dst-port 8080
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                   Instance: 93fd49ec-3113-4fa2-96f5-d16418da420f | Source IP: 0.0.0.0/0 | Protocol: any | Destination Port: 8080 | Direction: ingress | Status: Allowed                                   |
+----------------------------------------------+----------------------------------------------+----------------------+------------+---------------+------------------------+-----------------------+------------------------+
|              Security Group ID               |            Security Group Rule ID            |   Remote IP Prefix   |  Protocol  |   Port Range  |   Source IP Allowed?   |   Protocol Allowed?   |   Dest Port Allowed?   |
+----------------------------------------------+----------------------------------------------+----------------------+------------+---------------+------------------------+-----------------------+------------------------+
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     030cf802-622b-43af-a354-a42a1019760a     |      0.0.0.0/0       |    tcp     |    any:any    |          True          |          True         |          True          |
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     318584e3-b4f2-4cf9-9c22-8299a617586c     |      0.0.0.0/0       |    udp     |    any:any    |          True          |          True         |          True          |
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     531362cc-1e9d-46cc-8640-4db612d4606d     |      5.5.5.0/24      |    tcp     |     80:80     |          True          |          True         |         False          |
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     5512f55b-be90-4bfd-9ae2-0e9aa48acf3a     |      0.0.0.0/0       |    icmp    |    any:any    |          True          |          True         |          True          |
|     23ecf413-93fc-42fe-89ef-e0fafaa2f934     |     e07234d6-eb6e-4b31-909f-84aaca97ab7c     |      0.0.0.0/0       |    tcp     |     80:80     |          True          |          True         |         False          |
+----------------------------------------------+----------------------------------------------+----------------------+------------+---------------+------------------------+-----------------------+------------------------+

(neutron-utils) 🌕OpenStack Lab % ./secgrp.py --instance-uuid 93fd49ec-3113-4fa2-96f5-d16418da420f --protocol ah
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                    Instance: 93fd49ec-3113-4fa2-96f5-d16418da420f | Source IP: 0.0.0.0/0 | Protocol: ah | Destination Port: any | Direction: ingress | Status: Not Allowed                                    |
+-----------------------------------------------+-----------------------------------------------+----------------------+------------+---------------+-------------------------+-----------------------+-------------------------+
|               Security Group ID               |             Security Group Rule ID            |   Remote IP Prefix   |  Protocol  |   Port Range  |    Source IP Allowed?   |   Protocol Allowed?   |    Dest Port Allowed?   |
+-----------------------------------------------+-----------------------------------------------+----------------------+------------+---------------+-------------------------+-----------------------+-------------------------+
|      23ecf413-93fc-42fe-89ef-e0fafaa2f934     |      030cf802-622b-43af-a354-a42a1019760a     |      0.0.0.0/0       |    tcp     |    any:any    |           True          |         False         |           True          |
|      23ecf413-93fc-42fe-89ef-e0fafaa2f934     |      318584e3-b4f2-4cf9-9c22-8299a617586c     |      0.0.0.0/0       |    udp     |    any:any    |           True          |         False         |           True          |
|      23ecf413-93fc-42fe-89ef-e0fafaa2f934     |      531362cc-1e9d-46cc-8640-4db612d4606d     |      5.5.5.0/24      |    tcp     |     80:80     |           True          |         False         |          False          |
|      23ecf413-93fc-42fe-89ef-e0fafaa2f934     |      5512f55b-be90-4bfd-9ae2-0e9aa48acf3a     |      0.0.0.0/0       |    icmp    |    any:any    |           True          |         False         |           True          |
|      23ecf413-93fc-42fe-89ef-e0fafaa2f934     |      e07234d6-eb6e-4b31-909f-84aaca97ab7c     |      0.0.0.0/0       |    tcp     |     80:80     |           True          |         False         |          False          |
+-----------------------------------------------+-----------------------------------------------+----------------------+------------+---------------+-------------------------+-----------------------+-------------------------+
```
