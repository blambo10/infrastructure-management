#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from modules.awx import AnsibleAwx
from modules.network import Network

group_ids = {
    'linux': None,
    'windows': None,
    'other': None
}

net_util = Network('192.168.1.0', '24')

discovered_hosts = net_util.get_network_hosts()

linux_hosts = discovered_hosts.get('linux', None)
windows_hosts = discovered_hosts.get('windows', None)
other_hosts = discovered_hosts.get('other', None)

for group in group_ids:
    for discovered_host in discovered_hosts.get(group):
        print('OS: {}'.format(group))
        print('ID: {}'.format(group_ids.get(group)))
        print('Host: {}'.format(discovered_host))
        # print()
        # awx_util.create_host_inventory_in_group()

# https://{{ ansible_tower_host }}/api/v2/groups/{{ group_id }}/hosts/

