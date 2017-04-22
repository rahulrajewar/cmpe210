import urllib
import requests
import json
import time
import os

def topology_info():
	print '\n<----------------------------SUMMARY------------------------------>'
	data1 = requests.get("http://10.0.2.15:8080/wm/core/controller/summary/json")	
	dat1 = data1.json()
	number_of_switches = dat1 ["# Switches"]
	number_of_hosts = dat1 ["# hosts"]
	print '# Switches Connected: ', number_of_switches
	print '# Hosts Connected: ', number_of_hosts
	print '------------------------------------------------------------------\n'
	return( number_of_switches , number_of_hosts )

def switch_info ( number_of_switches , switch_dpids ):
	data = requests.get("http://10.0.2.15:8080/wm/core/controller/switches/json")
	dat = data.json()
	k=0
	for k in range( 0 , number_of_switches):
		DPID = dat [k]["switchDPID"]
		DPID = DPID.decode()
		switch_dpids.append(DPID)
	return (switch_dpids)

def host_info(number_of_hosts , hosts):
	a = requests.get("http://10.0.2.15:8080/wm/device/")
	b = a.json()
	for k in range( 0, number_of_hosts):		
		c = str(b["devices"][k]['ipv4'])
		if c != []:			
			hosts[str(c)] = str(b["devices"][k]["attachmentPoint"])
	return(hosts)

def switch_byte( number_of_switches, switch_dpids ):
	for k in range(0, number_of_switches):
		print switch_dpids[k]
		a = requests.get("http://10.0.2.15:8080/wm/core/switch/"+switch_dpids[k]+"/flow/json")
		b = a.json()
		print '\t Packet Count:', b["flows"][0]['packet_count']
		print '\t Cookie:', b["flows"][0]['cookie']
		print '\t byte count:', b["flows"][0]['byte_count']

def bandwidth ( switch_dpids, number_of_switches ):
	for k in range(	0, number_of_switches ):
		print switch_dpids[k]
		for port in range(1,5):
			try:				
				a = requests.get("http://10.0.2.15:8080/wm/statistics/bandwidth/"+switch_dpids[k]+"/"+str(port)+"/json")
				b = a.json()
				print "\tport :", b[0]["port"]
				bandwidth = b[0]["bits-per-second-rx"]
				print "\t\tBits per Second :", bandwidth
				if bandwidth > 15000:
					print 'adding static flow rule:'
					one = 'curl -X POST -d'
					two = '{"switch":"', switch_dpid[k]
					three = ', "name":"flow-mode-', k
					four = '", "cookie":"0", "priority":"32768", "in_port":"',port
					five = '", "active":"true", "actions":"no-forward"}'
					six = ' http://10.0.2.15:8080/wm/staticentrypusher/json'
					print one,two,three,four,five,six
					os.system(one,two,three,four,five,six)
					print 'flow rule added'
			except:
				print "port", port," no connected"

def stat_enable():

	try:
		stat = requests.put("http://10.0.2.15:8080/wm/statstics/config/enable/json")
		print "Enabled statistics..."

	except Exception as e:
		print"error while enabling statistics :" , e

def start():

	try:

		number_of_switches , number_of_hosts = topology_info();
		switch_dpids = list()
		hosts = dict()
		switch_dpids = switch_info ( number_of_switches, switch_dpids ) ;
		hosts = host_info ( number_of_hosts , hosts );
		switch_byte ( number_of_switches, switch_dpids );			
		bandwidth ( switch_dpids, number_of_switches );

	except Exception as e:
		print'Error occured', e

try:

	stat_enable();
	while 1:
		secs = 5
		time.sleep(secs)
		start()

except:
	print'Errorrrrrrrrrrrr'

#to access hosts info from dict


#	for k in range( 1, number_of_hosts-1):
#		k = str(k)
#		m = "[u'10.0.0."+ k +"']"
#		print hosts[m]
