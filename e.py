import urllib
import requests
import json
import time
import os
import threading

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
		bandwidth_one ( DPID, number_of_switches );
	return (switch_dpids)
	bandwidth_one ( DPID, number_of_switches );

def host_info(number_of_hosts , hosts):
	a = requests.get("http://10.0.2.15:8080/wm/device/")
	b = a.json()
	for k in range( 0, number_of_hosts):		
		c = str(b["devices"][k]['ipv4'])
		if c != []:			
			hosts[str(c)] = str(b["devices"][k]["attachmentPoint"])
	return(hosts)

def switch_byte( number_of_switches, switch_dpids ):
	try:
		for k in range(0, number_of_switches):
			print switch_dpids[k]
			a = requests.get("http://10.0.2.15:8080/wm/core/switch/"+switch_dpids[k]+"/flow/json")
			b = a.json()
			print '\t Packet Count:', b["flows"][0]['packet_count']
			print '\t Cookie:', b["flows"][0]['cookie']
			print '\t byte count:', b["flows"][0]['byte_count']
		return (0)
	except:
		return(switch_dpids[k])

def bandwidth_one ( DPID , number_of_switches ):
	print DPID
	for port in range(1,5):
		try:				
			a = requests.get("http://10.0.2.15:8080/wm/statistics/bandwidth/"+DPID+"/"+str(port)+"/json")
			b = a.json()
			print "\tport :", b[0]["port"]
			bandwidth = int (b[0]["bits-per-second-rx"])
			print "\t\tBits per Second :", bandwidth

			if bandwidth > 10000:
				print 'adding static flow rule:'
				one = 'curl -X POST -d'
				seven = "'"
				two = '{"switch":"' + DPID
				three = '", "name":"flow-mode-' + str(port)
				four = '", "cookie":"0", "priority":"32768", "in_port":"'+ str(port)
				five = '", "active":"true", "actions":"no-forward"}'
				eight = "'"
				six = ' http://10.0.2.15:8080/wm/staticentrypusher/json'
				command = one + seven + two + three + four + five + eight + six
				os.system(command)
				print command				
				print 'flow rule added'
		
		except:
			print "port", port," no connected"	

def Flowpusher(dpid):
	for port in range(1,3):
		print 'adding static flow rule:'
		one = 'curl -X POST -d'
		seven = "'"
		two = '{"switch":"' + dpid
		three = '", "name":"flow-mode-' + str(port)
		four = '", "cookie":"0", "priority":"32768", "in_port":"'+ str(port)
		five = '", "active":"true", "actions":"no-forward"}'
		eight = "'"
		six = ' http://10.0.2.15:8080/wm/staticentrypusher/json'
		command = one + seven + two + three + four + five + eight + six
		os.system(command)
		print command				
		print 'flow rule added'
	secs = 4
	time.sleep(secs)

def Flowremover(dpid):
	print ' Removing Flow entry'
	one = 'curl http://10.0.2.15:8080/wm/staticentrypusher/clear/'+ str(dpid) + '/json'
	os.system(one)
	print 'Removed all flow rules added for ' + str(dpid)
	secs = 10
	time.sleep(secs)
	global attack
	attack = False

def stat_enable():

	try:
		stat = requests.put("http://10.0.2.15:8080/wm/statistics/config/enable/json")
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
		dpid = switch_byte ( number_of_switches, switch_dpids );
		print 'dpid= ', dpid
		if dpid != 0:
			print'calling flow pusher'
			global attack
			attack = True
			attacked_switches.add(dpid)
			T2 = threading.Thread(target=Flowpusher, args=[dpid])
			T2.start()
		elif attack:
			T3 = threading.Thread(target=Flowremover, args=[dpid])
			T3.start()

	except Exception as e:
		print'Error occured:', e

def main():
	try:
		stat_enable();
		while 1:
			secs = 5
			time.sleep(secs)
			start()

	except:
		print'Error'
attack = False
T1 = threading.Thread(target=main)
T1.start()

