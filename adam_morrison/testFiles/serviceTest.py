import subprocess
import re

getInfo = subprocess.check_output('systemctl|grep running',shell=True)

check = r".*\.service"
check2 = r"systemd-.*\.service"

#All running services
runningServ = re.findall(check,getInfo)
print(runningServ)

#All running services with systemd as the first word
systemdServ = re.findall(check2,getInfo)
print(systemdServ)
