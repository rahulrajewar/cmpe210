import urllib
import requests
import httplib
import json

'''def bandwidth(dpid):
	for port in range(1,5):
		try:
			a = requests.get("http://10.0.2.15:8080/wm/statistics/bandwidth/"+dpid+"/"+str(port)+"/json")
			b = a.json()
			print "\tport :", b[0]["port"]
			print "\t\tLink Speed :", b[0]["link-speed-bits-per-second"]
			print "\t\tBits per Second :", b[0]["bits-per-second-rx"]
		except:
			print "port", port," no connected"

'''
def switch_info(dpid):
	
	a = requests.get("http://10.0.2.15:8080/wm/core/switch/"+dpid+"/flow/json")
	b = a.json()

	print '\t Packet Count:', b["flows"][0]['packet_count']

	print '\t Version: ', b["flows"][0]['version']

	print '\t Cookie:', b["flows"][0]['cookie']

	print '\t byte count:', b["flows"][0]['byte_count']

	print '\t Priority:', b["flows"][0]['priority']

	print '\t Controller action:', b["flows"][0]["instructions"]['instruction_apply_actions']['actions']
	

def switches(y):
	print '\n<------------------------Switches DPIDs--------------------------->'
	data = requests.get("http://10.0.2.15:8080/wm/core/controller/switches/json")
	dat = data.json()
	k=0
	for k in range(0,y):
		print'inetaddress = ', dat [k]["inetAddress"]
		dpid = dat [k]["switchDPID"]
		print'switch DPID = ', dpid
		dpid = dpid.decode()
		switch_info(dpid);
		#bandwidth(str(dpid));
	print '<----------------------------------------------------------------->\n'

def summary():
	print '\n<----------------------------SUMMARY------------------------------>'
	data1 = requests.get("http://10.0.2.15:8080/wm/core/controller/summary/json")	
	dat1 = data1.json()
	x = dat1 ["# Switches"]
	print '# Switches Connected: ', x
	print '# Hosts Connected: ',dat1 ["# hosts"]
	print '# inter-switch links: ', dat1 ["# inter-switch links"]
	print '# quarantine ports: ' , dat1 ["# quarantine ports"]
	print '<------------------------------------------------------------------>\n'
	return(x)
try:
	y = summary();
	switches(y);
except Exception as e:
	print'Error occured', e
