#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scapy.all as scapy
import os
import json
import argparse
import requests

from requests.auth import HTTPBasicAuth



#This needs to be put in its own class ALL needs to be put in a commons library for python
def call_http(url, username=None, password=None, port=None, uri=None, method='get', payload=None, tls=False):
    headers = {'Content-type': 'application/json'}
    req_url = 'http://{}'.format(url)

    if tls:
        req_url = 'https://{}'.format(url)

    if port:
        req_url = '{}:{}'.format(req_url, port)

    if uri:
        req_url = '{}{}'.format(req_url, uri)
    
    if method is 'get':
        response = requests.get(req_url, auth=HTTPBasicAuth(username, password))
    
    if method is 'post':
        response = requests.post(req_url, data=payload, headers=headers, auth=HTTPBasicAuth(username, password))
    
    # print()
    # if not response.status_code <= 200 <= 299:
    #     print('an error occured talking to remote http service') 
        # raise('an error occured talking to remote http service')

    try:
        response_data = response.json()
    except: 
        response_data = response
        
    return response_data

class AnsibleAwx:
    #"http://awx.thelabshack.com:8080/api/v2/groups/"

    def __init__(self, awx_address, awx_port, awx_username, awx_password):
        self._awx_address = awx_address
        self._awx_port = awx_port
        self._awx_username = awx_username
        self._awx_password = awx_password

        self._awx_base_payload = {
            "name": "",
            "description": "",
            "organization": 1,
            "kind": "",
            "host_filter": None,
            "variables": ""
        }


    def get_inventory_groups(self, name=None, inventory=None):
        uri = '/api/v2/groups/'
        
        if name:
            uri = '{}?name={}'.format(uri, name)

        if inventory:
            delimiter = '?'
           
            if delimiter in uri:
                delimiter = '&'

            uri = '{}{}inventories={}'.format(uri, delimiter, name)

        data = call_http(self._awx_address, 
                        username=self._awx_username, 
                        password=self._awx_password, 
                        port=self._awx_port, uri='/api/v2/groups/')

        return data.get('results')
    
    def get_inventories(self, name=None):
        uri = '/api/v2/inventories/'
        
        if name:
            uri = '{}?name={}'.format(uri, name)

        data = call_http(self._awx_address,
                        username=self._awx_username, 
                        password=self._awx_password, 
                        port=self._awx_port, 
                        uri=uri)
        return data.get('results')
        # print(data)
    
    def create_inventory(self, name):
        uri = '/api/v2/inventories/'

        new_inventory = self._awx_base_payload

        new_inventory.update({'name': name})

        data = call_http(self._awx_address, 
                        username=self._awx_username, 
                        password=self._awx_password, 
                        port=self._awx_port, 
                        uri=uri, method='post', 
                        payload=json.dumps(new_inventory))
        return data

    def create_inventory_group(self, name, inventory_id):
        uri = '/api/v2/groups/'
        
        payload = {
            "name": name,
            "description": "",
            "inventory": inventory_id,
            "variables": ""
        }

        data = call_http(self._awx_address, 
                        username=self._awx_username, 
                        password=self._awx_password,            
                        port=self._awx_port,
                        uri=uri, 
                        method='post', 
                        payload=json.dumps(payload)
                        )
        return data

    def create_host_inventory_in_group(self, name, group_id):
        uri = '/api/v2/groups/{}/hosts/'.format(group_id)
        
        payload = {
            "name": name,
            "description": "",
            "enabled": True,
            "variables": ""
        }

        data = call_http(self._awx_address, 
                        username=self._awx_username,
                        password=self._awx_password,          
                        port=self._awx_port, 
                        uri=uri, method='post',
                        payload=json.dumps(payload)
                        )
        return data

    def update_inventory(self, name):
        pass