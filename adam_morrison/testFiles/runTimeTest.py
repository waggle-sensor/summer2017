from datetime import datetime
from dateutil.parser import parse
import pytz
import datetime
import re
import subprocess


getInfo = subprocess.check_output('systemctl|grep running',shell=True)

check = r".*\.service"
check2 = r"systemd-.*\.service"

#All running services
runningServList = re.findall(check,getInfo)

#All running services with systemd as the first word
systemdServList = re.findall(check2,getInfo)

statusList = []
startTimeList =[]
upTime = []

for i in systemdServList:
    command = "systemctl status " + i
    status = subprocess.check_output(command,shell=True)
    statusList.append(status)

for j in statusList:
    active = r"\s*Active:\s*.*"
    #time = r"\d*h\s*\d*min|\d*h|\d*min\s*\d*s|\d*min|\d+s"
    time = r"since .*;"

    #time = time.replace("since ","")
    
    findActive = re.findall(active,j)
    findTime = re.findall(time,findActive[0])
    #print(findActive)
    #print(findTime)
    if findTime:
        startTimeList.append(findTime[0].replace("since ","").replace(";",""))
    else:
        startTimeList.append(None)

#for j in startTimeList:
#    print j


for k in startTimeList:
    if k:
        #Get current time in UTC
        ufCurrTime = datetime.datetime.utcnow()
        currTime = pytz.utc.localize(datetime.datetime.utcnow())

        #Format the service start time (uses arbitrary start time for now)
        ufStartTime = parse(k)
        startTime = ufStartTime.astimezone(pytz.timezone("UTC"))

        #Subtract the two values to get the run time of the process
        upTime.append(currTime - startTime)
    else:
        upTime.append(None)

for j in upTime:
    print j
    print j.total_seconds()
    print type(j)
    print "---------------"

