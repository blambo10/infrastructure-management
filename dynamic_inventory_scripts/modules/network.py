#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scapy.all as scapy
import json

class Network:
    def __init__(self, network, prefix):
        self._network = network
        self._prefix = prefix
        self._cidr = "{}/{}".format(network, prefix)

        self.fingerprint_ports = {
            'windows': 3389,
            'linux': 22,
        }

        self.discovered_hosts = {}

        self._init_arp()

    def _init_arp(self):
        arp_req_frame = scapy.ARP(pdst = self._cidr)
        broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
        self.broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame
    
    def _scan_arp(self, fingerprint=False):
        hosts = {
            'windows': [],
            'linux': [],
            'other': []
        }

        #[BL] Scan network for devices using ARP
        answered_list = scapy.srp(self.broadcast_ether_arp_req_frame, 
                                timeout = 1, 
                                verbose = False)[0]
   
        #[BL] Iterate found devices on network
        for i in range(0,len(answered_list)):
            ssh_status = False

            #[BL] Check device for port status
            socket_response = scapy.sr1(scapy.IP(dst=answered_list[i][1].psrc)/scapy.TCP(dport=self.fingerprint_ports.get('linux'), flags="S"),verbose=False, timeout=0.2)

            if socket_response:

                if hasattr(socket_response, 'flags'):

                    #[BL] If ssh open update ssh_status for this iteration
                    if socket_response[scapy.TCP].flags == 18:
                        ssh_status = True

            if ssh_status:

                hosts['linux'].append(answered_list[i][1].psrc)
            else:
                hosts['other'].append(answered_list[i][1].psrc)
            
            self.discovered_hosts.update(hosts)

    def get_network_hosts(self):
        self._scan_arp()
        return self.discovered_hosts

