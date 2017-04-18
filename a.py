import urllib
import requests
import json
a = requests.get("http://10.0.2.15:8080/wm/device/")
b = a.json()

json_string = str(b)

print'mac address of host 1'
print b["devices"][0]['mac']
x = b["devices"][0]['mac']
y = x[0].decode()
print y
print'mac address of host 2'
print b["devices"][1]['mac']
w = b["devices"][1]['mac']
e = w[0].decode()
print e
print'ip address of host 1'
print b["devices"][0]['ipv6']
q = b["devices"][0]['ipv6']
r = q[0].decode()
print r
print'ip address of host 2'
print b["devices"][1]['ipv6']
u = b["devices"][1]['ipv6']
i = u[0].decode()
print i
