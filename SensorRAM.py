import sys
import os
import psutil
import time
import socket
import requests
import json
import argparse
import uuid
import time

parser = argparse.ArgumentParser()
parser.add_argument("monitor", help="= Monitor address")
parser.add_argument("period", help="= messurement period (s)")
args = parser.parse_args()
data = {}

#########GET MAC and IP#############
mac_addresses = []

mac_num = hex(uuid.getnode()).replace('0x', '')
mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))

mac_address = mac
myip = requests.get('http://ip.42.pl/raw').text

#########GET RAM (MB)#############
def getRAM():
    ram = psutil.virtual_memory()

    total_ram = "%.2f" % (ram.total / pow(1024,2))
    used_ram = "%.2f" % (ram.used / pow(1024,2))
    ram_usage = (float(used_ram) * 100) / float(total_ram)
    ram_usage = "%.2f" % (ram_usage)
    return ram_usage

#########GET DATA################
def prepareData():
	data['MAC'] = mac_address
	data['IP'] = myip
	data['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
	data['value'] = getRAM()

#########SEND JSON###############
def sendJson():
	json_data = json.dumps(data)
	json_data = json.loads(json_data)
	url = str(args.monitor)
	payload = json_data
	headers = {'content-type': 'application/json'}
	print(json_data)
	response = requests.post(url, data=json.dumps(payload), headers=headers)
	print(response.text)

##########MAIN LOOP##############
while True:
	prepareData()
	sendJson()
	time.sleep(int(args.period))

