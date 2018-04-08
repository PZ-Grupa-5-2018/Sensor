import sys
import os
import psutil
import time
import socket
import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("measurement", help="= cpu, memory or disk")
args = parser.parse_args()
data = {}

#########GET MAC and IP#############
mac_addresses = []
nics = psutil.net_if_addrs()
nics.pop('lo')
for i in nics:
    for j in nics[i]:
        if j.family == 17:
            mac_addresses.append(j.address)

mac_address = mac_addresses[0]
myip = requests.get('http://ip.42.pl/raw').text

##########GET CPU (%)###############
def getCPU():
    all_cpus_usage=0
    time.sleep(1)
    cpus_count = psutil.cpu_count()
    cpus_percent = psutil.cpu_percent(percpu=True)
    for percent in cpus_percent:
        all_cpus_usage += float(percent)

    all_cpus_usage = all_cpus_usage / cpus_count
    all_cpus_usage = "%.2f" % (all_cpus_usage)
    return all_cpus_usage

#########GET RAM (MB)#############
def getRAM():
    ram = psutil.virtual_memory()

    total_ram = "%.2f" % (ram.total / pow(1024,2))
    used_ram = "%.2f" % (ram.used / pow(1024,2))
    return total_ram, used_ram

#########GET MEMORY (MB)##########
def getMemory():
    disk = psutil.disk_partitions(all=False)

    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        usage = psutil.disk_usage(part.mountpoint)
        break

    total_disk = "%.2f" % (usage.total / pow(1024,3))
    used_disk = "%.2f" % (usage.used / pow(1024,3))
    return total_disk, used_disk

#########GET DATA################
data['MAC'] = mac_address
data['IP'] = myip

if args.measurement == 'cpu':
    data['CPU'] = getCPU()
elif args.measurement == 'disk':
    data['DISK_TOTAL'] = getMemory()[0]
    data['DISK_USED'] = getMemory()[1]
elif args.measurement == 'memory':
    data['RAM_TOTAL'] = getRAM()[0]
    data['RAM_USED'] = getRAM()[1]
else:
    print("Wrong argument")
    sys.exit()

#########SEND JSON###############
json_data = json.dumps(data)

url = 'http://127.0.0.1:54321/measurement'
payload = json_data
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)



