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

##########GET CPU (%)###############
def getCPU():
    all_cpus_usage=0
    time.sleep(1)
    cpus_count = psutil.cpu_count()
    cpus_percent = psutil.cpu_percent(percpu=True)
    for percent in cpus_percent:
        all_cpus_usage += float(percent)

    all_cpus_usage = (cpus_count * 100) / all_cpus_usage
    all_cpus_usage = "%.2f" % (all_cpus_usage)
    return all_cpus_usage

#########GET DATA################
def prepareData():
	data['MAC'] = mac_address
	data['IP'] = myip
	data['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
	data['value'] = getCPU()

#########SEND JSON###############
def sendJson():
	json_data = json.dumps(data)
	json_data = json.loads(json_data)
	url = str(args.monitor)
	payload = json_data
	headers = {'Content-type': 'application/json'}
	print(json_data)
	response = requests.post(url, data=json.dumps(payload), headers=headers)
	print(response.text)

##########MAIN LOOP##############
while True:
	prepareData()
	sendJson()
	time.sleep(int(args.period))



