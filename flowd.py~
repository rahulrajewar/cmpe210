import os
DPID = '00:00:00:00:00:00:00:01'
port = '1'

one = 'curl -X POST -d'
seven = "'"
two = '{"switch":"' + DPID
three = '", "name":"flow-mode-' + port
four = '", "cookie":"0", "priority":"32768", "in_port":"'+ port
five = '", "active":"true", "actions":"no-forward"}'
eight = "'"
six = ' http://10.0.2.15:8080/wm/staticentrypusher/json'
command = one + seven + two + three + four + five + eight + six
os.system(command)
print 'flow rule added'
