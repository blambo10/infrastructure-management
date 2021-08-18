#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from modules.awx import AnsibleAwx
from modules.network import Network

required_inventory_name = 'thelabshack_core_infra_mgmt'

required_groups = [
    'linux',
    'windows',
    'other'
]

inventory_id = None
linux_group_id = None
windows_group_id = None
other_group_id = None

awx_util = AnsibleAwx('awx.thelabshack.com', 8080)
inventory = awx_util.get_inventories(name='thelabshack_core_infra_mgmt')

if not inventory:
    inventory_data = awx_util.create_inventory(name=required_inventory_name)

    inventory_id = inventory_data.get('id')

    for group in required_groups:
        awx_util.create_inventory_group(name=group, 
                                        inventory_id=inventory_id)

if inventory:
    
    inventory_id = inventory[0].get('id')

    groups = awx_util.get_inventory_groups(inventory=inventory_id)

    for group in groups:
        if group.get('name') is 'linux':
            linux_group_id = 'id'
        
        if group.get('name') is 'windows':
            windows_group_id = 'id'

        if group.get('name') is 'other':
            other_group_id = 'id'

    if not linux_group_id:
        data = awx_util.create_inventory_group(name='linux', inventory_id=inventory_id)
        # linux_group_id = data.get('id')

    if not windows_group_id:
        windows_group_id = awx_util.create_inventory_group(name='windows', inventory_id=inventory_id)
        # windows_group_id = data.get('id')

    if not other_group_id:
        data = awx_util.create_inventory_group(name='other', inventory_id=inventory_id)
        # other_group_id = data.get('id')

# print(json.dumps(group.get('name'), indent=4))

net_util = Network('192.168.1.0', '24')

discovered_hosts = net_util.get_network_hosts()

for discovered_host in discovered_hosts:
    awx_util.create_host_inventory_in_group()

# https://{{ ansible_tower_host }}/api/v2/groups/{{ group_id }}/hosts/

