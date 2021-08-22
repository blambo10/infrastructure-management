from pyunifiwsi import UnifiClient
import json

# endpoint = '/proxy/network/api/s/default/stat/sta'
endpoint = 'stat/device'

client = UnifiClient('', '', '192.168.1.9', 443, ssl_verify=False)
# client = UnifiClient('UxEeheDA5ZN3', '6mJUNZzULmhQqyNxGuXt', '192.168.1.1', 443, ssl_verify=False)

# print(dir(client.api))
# data = client.devices()
data = client.api(endpoint)
# data = client.api('api/s/system')


# api/s/default/stat/sta

# devices = client.devices()
# for device in devices:
# 	print(device.get('model'))
# data = json.loads(data[0])

print(data)
# print(json.dumps(data, indent=4, sort_keys=True))