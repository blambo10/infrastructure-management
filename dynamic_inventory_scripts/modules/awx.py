#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scapy.all as scapy
import os
import json
import argparse
import requests

from requests.auth import HTTPBasicAuth

#Move this to be moved to arguments in the constructor
awx_usernaame = os.environ('AWX_USERNAME')
awx_password = os.environ('AWX_PASSWORD')

#This needs to be put in its own class ALL needs to be put in a commons library for python
def call_http(url, port=None, uri=None, tls=False):
    req_url = 'http://{}'.format(url)

    if tls:
        req_url = 'https://{}'.format(url)

    if port:
        req_url = '{}:{}'.format(req_url, port)

    if uri:
        req_url = '{}{}'.format(req_url, uri)
    
    response = requests.get(req_url, auth=HTTPBasicAuth(awx_usernaame, awx_password))
    response_data = response.json()

    return response_data

class AnsibleAwx:
    #"http://awx.thelabshack.com:8080/api/v2/groups/"

    def __init__(self, awx_address, awx_port):
        self._awx_address = awx_address
        self._awx_port = awx_port

    def get_inventory_groups(self, name=None, inventory=None):
        uri = '/api/v2/groups/'
        
        if name:
            uri = '{}?name={}'.format(uri, name)

        if inventory:
            delimiter = '?'
           
            if delimiter in url:
                delimiter = '&'

            uri = '{}{}inventories={}'.format(uri, delimiter, name)

        data = call_http(self._awx_address, port=self._awx_port, uri='/api/v2/groups/')
        return data.get('results')
    
    def get_inventories(self, name=None):
        uri = '/api/v2/inventories/'
        
        if name:
            uri = '{}?name={}'.format(uri, name)

        data = call_http(self._awx_address, port=self._awx_port, uri=uri)
        return data.get('results')
        # print(data)
    
    def create_inventory_group(self):
        pass