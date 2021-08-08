from pyunifiwsi import UnifiClient
import json

client = UnifiClient('', '', '', 443, ssl_verify=False)

data = client.get_devices()

# devices = client.devices()
# for device in devices:
# 	print(device.get('model'))
# data = json.loads(data[0])

print(data)
