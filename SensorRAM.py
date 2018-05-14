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
import platform
import threading

parser = argparse.ArgumentParser()
parser.add_argument("monitor", help="= Monitor address")
parser.add_argument("period", help="= Messurement period (s)")
parser.add_argument("name", help="= Host name")
parser.add_argument("metricsName", help="= Metrics name")
args = parser.parse_args()
data = {}
hostID = 0
metricType = 2
metricID = 0

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
def prepareSensorData():
	data['MAC'] = mac_address
	data['IP'] = myip
	data['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
	data['value'] = getRAM()

#########PREPARE SENSOR REGISTER DATA################
def prepareRegisterData():
	platform.processor()
	data['mac'] = mac_address
	data['ip'] = myip
	data['name'] = args.name
	data['cpu'] = str(platform.processor())
	ram = psutil.virtual_memory()
	total_ram = "%.2f" % (ram.total / pow(1024,2))
	data['memory'] = total_ram

#########PREPARE MEASUREMENT REGISTER DATA################
def prepareMeasurementData():
	data['metric_id'] = str(metricType)
	data['type'] = str(args.metricsName)
	data['period_seconds'] = args.period

#########REGISTER SENSOR#########
def registerSensor():
	prepareRegisterData()
	sendJsonRegister(str(args.monitor + "/hosts/"))

#########REGISTER MEASUREMENT#########
def registerMeasurement():
	prepareMeasurementData()
	sendJsonMeasurement(str(args.monitor + "/hosts/" + str(hostID) + "/metrics/"))

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
	print(response.text)

#########SEND JSON###############
def sendJsonMeasurement(address):
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
	global metricID
	metricID = json_data_response['id']
	print(response.text)

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
	print(response.text)

registerSensor()
data={}
registerMeasurement()
data={}
##########MAIN LOOP##############
while True:
	prepareSensorData()
	sendJson(str(args.monitor + "/hosts/" + str(hostID) + "/metrics/" + str(metricID) + "/measurements/"))
	time.sleep(int(args.period))





