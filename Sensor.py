import sys
import os
import psutil
import time
import socket
import requests
import json

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
all_cpus_usage=0
time.sleep(1)
cpus_count = psutil.cpu_count()
cpus_percent = psutil.cpu_percent(percpu=True)
for percent in cpus_percent:
    all_cpus_usage += float(percent)

all_cpus_usage = all_cpus_usage / cpus_count
all_cpus_usage = "%.2f" % (all_cpus_usage)

#########GET RAM (MB)#############
ram = psutil.virtual_memory()

total_ram = "%.2f" % (ram.total / pow(1024,2))
used_ram = "%.2f" % (ram.used / pow(1024,2))

#########GET MEMORY (MB)##########
disk = psutil.disk_partitions(all=False)

for part in psutil.disk_partitions(all=False):
    if os.name == 'nt':
        if 'cdrom' in part.opts or part.fstype == '':
            continue
    usage = psutil.disk_usage(part.mountpoint)
    break

total_disk = "%.2f" % (usage.total / pow(1024,3))
used_disk = "%.2f" % (usage.used / pow(1024,3))

###########JSON###################
data = {}
data['MAC'] = mac_address
data['IP'] = myip
data['CPU'] = all_cpus_usage
data['RAM_TOTAL'] = total_ram
data['RAM_USED'] = used_ram
data['DISK_TOTAL'] = total_disk
data['DISK_USED'] = used_disk

json_data = json.dumps(data)
print(json_data)

#########SEND JSON###############
#TODO
#url = ''
#payload = json_data
#headers = {'content-type': 'application/json'}

#response = requests.post(url, data=json.dumps(payload), headers=headers)
#response.status_code


