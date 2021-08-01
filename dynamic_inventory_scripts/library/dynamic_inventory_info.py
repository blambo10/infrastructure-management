#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2015, Joseph Callen <jcallen () csc.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dynamic_inventory_info
short_description: Scan local network for inventory
description:
    - Scan network for inventory and update awx via api
version_added: '1.0'
author:
- Bryce Lamborne
requirements:
    - pyscapy and argparse installed
options:
    cluster_name:
        description:
            - The name of the cluster that will be created.
        required: yes
    datacenter_name:
        description:
            - The name of the datacenter the cluster will be created in.
        required: yes
'''

EXAMPLES = r'''
- name: Update Inventory
  dynamic_inventory_info: 
    scan_network: '192.168.1.0/24'
    scan_port: 22
  delegate_to: localhost
'''

try:
    import scapy.all as scapy
    HAS_SCAPY = True
except ImportError:
    HAS_DEPS = False

try:
    import argparse
    HAS_ARGPARSE = True
except ImportError:
    HAS_ARGPARSE = False


from ansible.module_utils.basic import AnsibleModule

class DynamicInventory(object):
    def __init__(self, module):
        self.module = module
        self.scan_network = module.params['cluster_name']
        self.scan_port = module.params['datacenter_name']
        # self.enable_drs = module.params['enable_drs']
        # self.enable_ha = module.params['enable_ha']
        # self.enable_vsan = module.params['enable_vsan']
        # self.desired_state = module.params['state']
        self.content = host_discovery(module)

    def host_discovery(self):
        arp_req_frame = scapy.ARP(pdst = self.scan_network)

        broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")

        broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

        #[BL] Scan network for devices using ARP
        answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]
        ansible_groups = {}
        discovered_hosts = []

        #[BL] Iterate found devices on network
        for i in range(0,len(answered_list)):
            ssh_status = False

            #[BL] Check device for port status
            socket_response = scapy.sr1(scapy.IP(dst=answered_list[i][1].psrc)/scapy.TCP(dport=self.scan_port, flags="S"),verbose=False, timeout=0.2)

            if socket_response:

                if hasattr(socket_response, 'flags'):

                    #[BL] If ssh open update ssh_status for this iteration
                    if socket_response[scapy.TCP].flags == 18:
                        ssh_status = True

            if ssh_status:

                discovered_hosts.append(answered_list[i][1].psrc)

            # client_dict = {
            #     "ip" : answered_list[i][1].psrc,
            #     "mac" : answered_list[i][1].hwsrc,
            #     "ssh": ssh_status
            # }

        ansible_groups.update({
            'linux':{
                'hosts': discovered_hosts,
                'vars': {
                    'var1': True
                },
                'children':[]
            }
        })

        return ansible_groups



def main():

    argument_spec.update(dict(
        scan_network=dict(type='str', required=True),
        scan_port=dict(type='int', required=True)
        # state=dict(type='str', default='present', choices=['absent', 'present']),
    ))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if not HAS_ARGPARSE:
        module.fail_json(msg='argparse python module not found')

    if not HAS_SCAPY:
        module.fail_json(msg='scapy python module not found')

    inventory = DynamicInventory(module)
    discovered_inventory = inventory.host_discovery()

    module.exit_json(instance=discovered_inventory)


if __name__ == '__main__':
    main()
