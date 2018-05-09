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
parser.add_argument("period", help="= Messurement period (s)")
parser.add_argument("name", help="= Host name")
parser.add_argument("cpu", help="= CPU name")
parser.add_argument("memory", help="= Memory size")
args = parser.parse_args()
data = {}
hostID = 0
metricID = 1

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

#########PREPARE SENSOR DATA################
def prepareSensorData():
	data['mac'] = mac_address
	data['ip'] = myip
	data['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
	data['value'] = getCPU()

#########PREPARE SENSOR REGISTER DATA################
def prepareRegisterData():
	data['mac'] = mac_address
	data['ip'] = myip
	data['name'] = args.name
	data['cpu'] = args.cpu
	data['memory'] = args.memory

#########PREPARE MEASUREMENT REGISTER DATA################
def prepareMeasurementData():
	data['metric_id'] = metricID
	data['type'] = 'mean'
	data['period_seconds'] = args.period

#########REGISTER SENSOR#########
def registerSensor():
	prepareRegisterData()
	sendJsonRegister(str(args.monitor + "/hosts/"))

#########REGISTER MEASUREMENT#########
def registerMeasurement():
	prepareMeasurementData()
	sendJson(str(args.monitor + "/hosts/" + str(hostID) + "/metrics/"))

#########SEND JSON###############
def sendJsonRegister(address):
	print(address)
	json_data = json.dumps(data)
	json_data = json.loads(json_data)
	url = address
	payload = json_data
	headers = {'Content-type': 'application/json'}
	print(json_data)
	response = requests.post(url, data=json.dumps(payload), headers=headers)
	json_data_response = json.loads(response.text)
	print(json_data_response['id'])
	global hostID
	hostID = json_data_response['id']

#########SEND JSON###############
def sendJson(address):
	print(address)
	json_data = json.dumps(data)
	json_data = json.loads(json_data)
	url = address
	payload = json_data
	headers = {'Content-type': 'application/json'}
	print(json_data)
	response = requests.post(url, data=json.dumps(payload), headers=headers)
	json_data_response = json.loads(response.text)

registerSensor()
data={}
registerMeasurement()
data={}
##########MAIN LOOP##############
while True:
	prepareSensorData()
	sendJson(str(args.monitor + "/hosts/" + str(hostID) + "/metrics/" + str(metricID) + "/measurements/"))
	time.sleep(int(args.period))




