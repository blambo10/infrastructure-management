#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from modules.awx import AnsibleAwx
from modules.network import Network

required_inventory_name = 'thelabshack_core_infra_mgmt'

required_group_ids = {
    'linux': None,
    'windows': None,
    'other': None
}

inventory_id = None
linux_group_id = None
windows_group_id = None
other_group_id = None

awx_util = AnsibleAwx('awx.thelabshack.com', 8080)
inventory = awx_util.get_inventories(name='thelabshack_core_infra_mgmt')

if not inventory:

    inventory = awx_util.create_inventory(name=required_inventory_name)

    inventory_id = inventory.get('id')

    for group in required_group_ids.keys():
        awx_util.create_inventory_group(name=group, 
                                        inventory_id=inventory_id)

if inventory:

    inventory_id = inventory[0].get('id')

    retreived_groups = awx_util.get_inventory_groups(inventory=inventory_id)

    for group in retreived_groups:

        if group.get('name') == 'linux':
            linux_group_id = group.get('id')

            id_update = {
                'linux': linux_group_id
            }
            
            required_group_ids.update(id_update)
        
        if group.get('name') == 'windows':
            id_update = {
                'windows': group.get('id')
            }

            required_group_ids.update(id_update)            

        if group.get('name') == 'other':
            id_update = {
                'other': group.get('id')
            }
            
            required_group_ids.update(id_update)  

    # exit()

    if not required_group_ids.get('linux'):
        data = awx_util.create_inventory_group(name='linux', inventory_id=inventory_id)
        # linux_group_id = data.get('id')

    if not required_group_ids.get('windows'):
        windows_group_id = awx_util.create_inventory_group(name='windows', inventory_id=inventory_id)

    if not required_group_ids.get('other'):
        data = awx_util.create_inventory_group(name='other', inventory_id=inventory_id)

net_util = Network('192.168.1.0', '24')

discovered_hosts = net_util.get_network_hosts()

linux_hosts = discovered_hosts.get('linux', None)
windows_hosts = discovered_hosts.get('windows', None)
other_hosts = discovered_hosts.get('other', None)

for group in required_group_ids.keys():
    for discovered_host in discovered_hosts.get(group):
        print('OS: {}'.format(group))
        print('ID: {}'.format(required_group_ids.get(group)))
        print('Host: {}'.format(discovered_host))
        awx_util.create_host_inventory_in_group(discovered_host, required_group_ids.get(group))