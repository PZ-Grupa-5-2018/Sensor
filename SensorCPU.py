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
parser.add_argument("metricsName", help="= Metrics name")
parser.add_argument("--autoOffPeriod", help="= Auto off period (s)")
args = parser.parse_args()
data = {}
hostID = 0
metricType = 1
metricID = 0

#########GET MAC and IP#############
mac_addresses = []

mac_num = hex(uuid.getnode()).replace('0x', '')
mac_num = mac_num.zfill(12)
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

    all_cpus_usage = all_cpus_usage / cpus_count
    all_cpus_usage = "%.2f" % (all_cpus_usage)
    return all_cpus_usage

#########PREPARE SENSOR DATA################
def prepareSensorData():
	data['mac'] = mac_address
	data['ip'] = myip
	data['value'] = getCPU()
	data['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

#########PREPARE SENSOR REGISTER DATA################
def prepareRegisterData():
	platform.processor()
	data['mac'] = mac_address
	data['ip'] = myip
	data['name'] = str(platform.node())
	data['cpu'] = str(platform.processor())
	ram = psutil.virtual_memory()
	total_ram = "%.2f" % (ram.total / pow(1024,2))
	data['memory'] = total_ram
	data['platform'] = str(platform.system() + " " + platform.release())

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

##########THREAD FUNCTION########
def getAndSend():
	prepareSensorData()
	sendJson(str(args.monitor + "/hosts/" + str(hostID) + "/metrics/" + str(metricID) + "/measurements/"))


##########MAIN LOOP##############
if not args.autoOffPeriod:
    while True:
	    th = threading.Thread(target=getAndSend, args=[])
	    th.start()
	    time.sleep(int(args.period))
else:
    loops = int(args.autoOffPeriod) // int(args.period)
    for i in range(loops):
        th = threading.Thread(target=getAndSend, args=[])
        th.start()
        time.sleep(int(args.period))





