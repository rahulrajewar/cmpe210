import urllib
import requests
import json

def switch_info():
	print '--------------------------Switch Stat----------------------------------\n'
	a = requests.get("http://10.0.2.15:8080/wm/core/switch/00:00:00:00:00:00:00:01/flow/json")
	b = a.json()

	print 'Packet Count:', b["flows"][0]['packet_count']

	print 'Version: ', b["flows"][0]['version']

	print 'Cookie:', b["flows"][0]['cookie']

	print 'byte count:', b["flows"][0]['byte_count']

	print 'Priority:', b["flows"][0]['priority']

	print 'Controller action:', b["flows"][0]["instructions"]['instruction_apply_actions']['actions']
	print '------------------------------------------------------------------\n'

def switches(y):
	print '\n<----------------------------Switches DPIDs------------------------------>'
	data = requests.get("http://10.0.2.15:8080/wm/core/controller/switches/json")
	dat = data.json()
	k=0
	for k in range(0,y):
		print'inetaddress = ', dat [k]["inetAddress"]
		print'switch DPID = ', dat [k]["switchDPID"]
	print '------------------------------------------------------------------\n'

def summary():
	print '\n<----------------------------SUMMARY------------------------------>'
	data1 = requests.get("http://10.0.2.15:8080/wm/core/controller/summary/json")	
	dat1 = data1.json()
	x = dat1 ["# Switches"]
	print '# Switches Connected: ', x
	print '# Hosts Connected: ',dat1 ["# hosts"]
	print '# inter-switch links: ', dat1 ["# inter-switch links"]
	print '# quarantine ports: ' , dat1 ["# quarantine ports"]
	print '------------------------------------------------------------------\n'
	return(x)
try:
	y = summary();
	switches(y);
	switch_info();
except:
	print'Error occured'
