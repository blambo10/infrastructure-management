#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import scapy.all as scapy
import argparse

SCAN_NETWORK="192.168.1.0/24"
PORT = 22

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', help='list host vars',required=False)
    parser.add_argument('--list', action='store_true', help='list all hosts in ansible format')
    arguments = parser.parse_args()

    return arguments

def host_discovery(ip):
    arp_req_frame = scapy.ARP(pdst = ip)

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
        socket_response = scapy.sr1(scapy.IP(dst=answered_list[i][1].psrc)/scapy.TCP(dport=PORT, flags="S"),verbose=False, timeout=0.2)

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

def show_hosts(result):
    print(result)

if __name__ == '__main__':
    arguments = get_args()
    if arguments.host:
        host_vars = {
            "_meta": {
                "hostvars": {}
            }
        }

        print(host_vars)

    if arguments.list:
        discovered_hosts = host_discovery(SCAN_NETWORK)
        show_hosts(discovered_hosts)

