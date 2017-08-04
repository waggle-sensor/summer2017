import subprocess
import re

runningServ = subprocess.check_output('systemctl|grep running',shell=True)
systemdServList = re.findall(r"systemd-.*\.service",runningServ)

statusList = []

for i in systemdServList:
    command = "systemctl status " + i
    status = subprocess.check_output(command,shell=True)
    print status
    statusList.append(status)



for j in statusList:
    active = r"\s*Active:\s*.*"
    time = r"\d*h\s*\d*min|\d*h"

    findActive = re.findall(active,j)
    findTime = re.findall(time,findActive[0])
    print(findActive)
    print(findTime)


    
'''
getInfo = subprocess.check_output('systemctl status systemd-journald.service',shell=True)

print(getInfo)

check = r"\s*Active:\s*.*"
check2 = r"\d*h\s*\d*min"

bleh = re.findall(check,getInfo)
bleh2 = re.findall(check2,bleh[0])
print(bleh)
print(bleh2[0])


check2 = r"systemd-.*\.service"
#All running services with systemd as the first word
systemdServList = re.findall(check2,getInfo)

'''
