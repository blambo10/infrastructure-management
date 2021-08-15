# from jnpr.junos import Device
# import json

# # print(dir(Device))
# # exit()
# with Device(host='192.168.1.201', user='', password='') as dev:
#     print (json.dumps(dev.facts))

from scapy.all import *
load_module("nmap")

target = '192.168.1.17'

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

open('nmap-os-fingerprints', 'wb').write(urlopen('https://raw.githubusercontent.com/nmap/nmap/9efe1892/nmap-os-fingerprints').read())
conf.nmap_base = 'nmap-os-fingerprints'

# result = nmap_fp(target,oport=22,cport=1)
result = nmap_fp(target,oport=63894,cport=1)

# result = nmap_fp(target)

print(result)