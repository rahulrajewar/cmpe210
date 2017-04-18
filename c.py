import urllib
import requests
import httplib
import json
import subprocess

class StaticFlowPusher(object):
  
    def __init__(self, server):
        self.server = server
  
    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])
  
    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200
  
    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200
  
    def rest_call(self, data, action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret

'''def switch(dpid):
	a = requests.get("http://10.0.2.15:8080/wm/device/")
	b = a.json()
	c = str(b)
	match = dpid
	scount = c.count(match)
	if scount > 0:
		for k in range(1,scount):
			print'Mac address switch:', k
			print b["devices"][k]['mac']
			print'IP address switch:', k
			print b["devices"][k]['ipv6']


def flow_pusher(dpid):
	flow_x = {"switch": dpid, "cookie":"69"}
	print'1'
	subprocess.call([
		'curl', '-X', 'POST', '-d', flow_x, 
		'http://10.0.2.15:8080/wm/staticflowpusher/json'])
	data = '{"switch": dpid, "cookie":"69"}'
	url = "http://10.0.2.15:8080/wm/staticflowpusher/json"
	req = urllib.Request(url, data , {'Content-Type':'application/json'}
	f = urllib.urlopen(req)
	for x in f:
		print x
	f.close()
'''
	
def switch_cookie(dpid):
	url = "http://10.0.2.15:8080/wm/core/switch/" + dpid + "/flow/json"
	a = requests.get(url)	
	b = a.json()
	cookie = b["flows"][0]['cookie']
	I_cookie = int(cookie)
	if I_cookie == 0:
		pusher = StaticFlowPusher('10.0.2.15')
		flow1 = {
    'switch':dpid,
    "name":"flow_mod_1",
    "cookie":"1",
    "priority":"1768",
    "in_port":"1",
    "active":"true",
    "actions":"output=flood"
    }
		pusher.set(flow1)
		print 1
		print I_cookie
	
def switches(y):
	data = requests.get("http://10.0.2.15:8080/wm/core/controller/switches/json")
	dat = data.json()
	k=0
	for k in range(0,y):
		dpid = dat [k]["switchDPID"]
		print 'switch DPID = ', dpid
		switch_cookie(dpid);


def summary():
	data1 = requests.get("http://10.0.2.15:8080/wm/core/controller/summary/json")	
	dat1 = data1.json()
	x = dat1 ["# Switches"]
	print '\n # Switches Connected: ', x ,'\n'
	return(x)

try:
	y = summary();
	switches(y);
except:
	print'Error occured'
