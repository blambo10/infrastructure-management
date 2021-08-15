#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from modules.awx import AnsibleAwx
from modules.network import Network

inventory_id = None
linux_group_id = None
windows_group_id = None
other_group_id = None

awx_util = AnsibleAwx('awx.thelabshack.com', 8080)
inventory = awx_util.get_inventories(name='thelabshack_core_infra_mgmt')

if not inventory:
    #write logic
    pass

if inventory:
    
    inventory_id = inventory[0].get('id')

    groups = awx_util.get_inventory_groups(inventory=inventory_id)

    for group in groups:
        if group.get('name') is 'linux':
            linux_group_id = 'id'
        
        if group.get('name') is 'windows':
            windows_group_id = 'id'

        if group.get('other') is 'other':
            other_group_id = 'id'


print(linux_group_id)
# print(json.dumps(group.get('name'), indent=4))

# net_util = Network('192.168.1.0', '24')
# print(net_util.get_network_hosts())