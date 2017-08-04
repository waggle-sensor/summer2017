from dateutil.parser import parse
from datetime import datetime

import subprocess
import datetime
import json
import time
import pytz
import re


def readfile(filename):
    with open(filename, 'r') as f:
        return f.read()


def getGeneralInfo():
    #get general info about node using 'hostnamectl'

    #get list of general info about node with 'hostnamectl' command
    getHostName = str(subprocess.check_output('hostnamectl', shell=True).decode('ascii'))

    #Use this RE (regular expression) pattern to find each metric
    pattern = r"\s*[a-zA-Z]*:\s*.\n|\s*[a-zA-Z]*\s*[a-zA-Z]*:\s*.*\n"
    info = re.findall(pattern,getHostName)

    genInfoList = {}

    #for loop that takes the name of the metric given in the 'hostnamectl' cmd and uses it as a key;
    #the value of the metric is the value in the dictionary
    for i in info:
        metricRE = r"\s*[a-zA-Z]*:|\s*[a-zA-Z]*\s*[a-zA-Z]*:"
        valueRE = r":\s*.*\n"
        metric = re.findall(metricRE, i)
        value = re.findall(valueRE, i)

        #replace empty spaces and colons with "" (nothing)
        genInfoList.update({metric[0].replace(":","").replace(" ",""):value[0].replace(": ","").replace("\n","")})

    #return general info about node as dictionary
    return genInfoList


def getNodeUptime():
    uptimeCmd = readfile('/proc/uptime')

    # find all occurences of numbers from upTimeCmd; the first one will be the uptime of the node and the second is ignored
    uptime = re.findall(r'\d*\.\d*', uptimeCmd)

    return {
        'UptimeSeconds': uptime[0],
        'UptimeFormatted': str(datetime.timedelta(seconds=int(float(uptime[0])))),
    }


def getUSBDevs():
    #get USB devices that are connected to node

    #use the 'lsusb' command to get the USB devices connected to the node
    getDevs = str(subprocess.check_output('lsusb',shell=True).decode('ascii'))

    pattern = r"Bus\s*\d+\s*Device\s*\d+:\s*ID.+"
    info = re.findall(pattern,getDevs)

    devs = {}

    #for loop that assigns each USB device a name (used as the key) in the format 'USBDev#';
    #the value in the dictionary is each device recognized by 'lsusb' command
    for i in range(0,len(info)):
        metricRE = r"Bus\s*\d+\s*Device\s*\d+:"
        valueRE = r"Bus\s*\d+\s*Device\s*\d+:.*"
        metric = "USBDev"+str(i)
        value = re.findall(valueRE, info[i])

        #update the dictioary with the next USB device and replace the colon with ""
        devs.update({metric:value[0].replace(": ","")})

    #return USB devices as dictionary
    return devs


def getMemInfo():
    #get memory (RAM) info from node
    memInfoList = {}

    #get memory info from /proc/meminfo file
    getInfo = str(subprocess.check_output('cat /proc/meminfo', shell=True).decode('ascii'))

    #RE's for total memory and free memory
    memFreeRE = r"MemFree:\s*.*\n"
    memTotalRE = r"MemTotal:\s*.*\n"

    #use the RE's to find MemFree and MemTotal in getInfo
    memFreeInfo = re.findall(memFreeRE,getInfo)
    memTotalInfo = re.findall(memTotalRE,getInfo)

    #remove the titles of each metric so we only have the values
    memFree = re.sub(r"MemFree:\s*","",memFreeInfo[0])
    memTotal = re.sub(r"MemTotal:\s*","",memTotalInfo[0])

    #remove "\n" from both metrics
    memFree = memFree.replace("\n","")
    memTotal = memTotal.replace("\n","")

    #return metrics as a dictionary
    memInfoList = {"MemFree":memFree,"MemTotal":memTotal}

    return memInfoList


def getCPUInfo():
    #get CPU info from node
    getInfo = str(subprocess.check_output('cat /proc/cpuinfo', shell=True).decode('ascii'))

    #RE's to find the number of CPU cores, vendor ID, and model name of the node (only for desktop computer testing)
    coreRE = r"cpu cores\s*:.*"
    vendorRE = r"vendor_id\s*:.*"
    modelRE = r"model name\s*:.*"

    #if/elif statements that determines if the code is running on a node, or a desktop for testing
    if re.search(vendorRE,getInfo):
        #find the num CPU cores, vendor ID, and model name of processor if on a testing desktop
        vendorInfo = str(re.search(vendorRE,getInfo).group(0))
        cpuInfo = str(re.search(coreRE,getInfo).group(0))
        modelInfo = str(re.search(modelRE,getInfo).group(0))

        cpuCores = re.sub(r"cpu cores\s*:\s*", "", cpuInfo)
        vendorId = re.sub(r"vendor_id\s*:\s*", "", vendorInfo)
        modelName = re.sub(r"model name\s*:\s*", "", modelInfo)

        #add metrics to the dictionary
        cpuInfo = {"CPUCores":cpuCores,"VendorID":vendorId,"ModelName":modelName}

    elif re.findall(r"Processor\s*:\s*.*",getInfo):
        #if on a node, only find the processor name (more metrics can be grabbed if needed)
        procInfo = re.findall(r"Processor\s*:\s*.*",getInfo)

        procOne = procInfo[0]
        proc = re.sub(r".*:","",procOne)

        #add metric to dictionary
        cpuInfo = {"Processor":str(proc)}

    #return CPU info as a dictionary
    return cpuInfo


def getDiskInfo():
    mountedDevs = []
    #get information about disks on node

    #run the detectDiskDevices.sh script located in current directory to detect which media the node is booted from
    getDevices = str(subprocess.check_output('~/waggleWebAPI/detectDiskDevices.sh', shell=True).decode('ascii'))
    pattern = r".*memory card not recognized.*"

    #if/else statement that determines if on a node, or on a desktop for testing
    if (re.search(pattern, getDevices)):
        #assign each metric the value of 'test' since it is not a node and no eMMC or SD card will be recognized
        currDiskName = "test"
        otherDiskName = "test"
        currDiskType = "test"
        otherDiskType = "test"
        currentDiskUsed = "test"
        currentDiskFree = "test"
        currentDiskUsage = "test"

        #add metrics to dictionary
        diskInfo = {"CurrentDiskName":currDiskName,"OtherDiskName":otherDiskName,"CurrentDiskType":currDiskType,"OtherDiskType":otherDiskType,"CurrentDiskUsed":str(currentDiskUsed),"CurrentDiskFree":str(currentDiskFree),"CurrentDiskUsage":str(currentDiskUsage)}

    else:
        #if on a node, the detectDiskDevices.sh script will return these four metrics, among others
        currDev = re.findall(r"CURRENT_DISK_DEVICE_NAME=.*",getDevices)
        otherDev = re.findall(r"OTHER_DISK_DEVICE_NAME=.*",getDevices)
        currType = re.findall(r"CURRENT_DISK_DEVICE_TYPE=.*",getDevices)
        otherType = re.findall(r"OTHER_DISK_DEVICE_TYPE=.*",getDevices)

        #format the retrieved metrics to remove the titles and only have the values of each metric remaining
        currDiskName = currDev[0].replace("CURRENT_DISK_DEVICE_NAME=","")
        otherDiskName = otherDev[0].replace("OTHER_DISK_DEVICE_NAME=","")
        currDiskType = currType[0].replace("CURRENT_DISK_DEVICE_TYPE=","")
        otherDiskType = otherType[0].replace("OTHER_DISK_DEVICE_TYPE=","")

        #find the disk/partition that the node is currently booted from
        devs = str(subprocess.check_output("mount | grep 'on /' |cut -f 1 -d ' ' | grep -o '/dev/mmcblk[0-1]p[0-2]'",shell=True).decode('ascii'))
        mountedDevs = re.findall(r"/dev/mmcblk[0-1]p[0-2]",devs)

        # assumes only ONE partition from ONE boot media is mounted; if this changes, there will be errors
        currPart = mountedDevs[0]

        #get and parse out each disk usage metric using 'df' command
        used = str(subprocess.check_output("df -k | grep " + currPart + " | awk '{print $3}'",shell=True).decode('ascii'))
        total = str(subprocess.check_output("df -k | grep " + currPart + " | awk '{print $2}'",shell=True).decode('ascii'))
        available = str(subprocess.check_output("df -k | grep " + currPart + " | awk '{print $4}'",shell=True).decode('ascii'))
        usage = str(subprocess.check_output("df -k | grep " + currPart + "| awk '{print $5}'",shell=True).decode('ascii'))

        #format the values to be read as Gigabytes rather than bytes
        currentDiskUsed = (float(used) * float(1024)) * float(10**-9)
        currentDiskFree = (float(available) * float(1024)) * float(10**-9)
        currentDiskUsage = usage.replace("\n","")

        #add metrics to the dictionary
        diskInfo = {"CurrentDiskName":currDiskName,"OtherDiskName":otherDiskName,"CurrentDiskType":currDiskType,"OtherDiskType":otherDiskType,"CurrentDiskUsed":str(currentDiskUsed)+"GB","CurrentDiskFree":str(currentDiskFree)+"GB","CurrentDiskUsage":str(currentDiskUsage)}

    #retunr disk info as a dictionary
    return diskInfo


def getRunningServices():
    #get running services on node and get their uptimes
    statusList = []
    services = {}

    getInfo = str(subprocess.check_output("systemctl|grep '.service.*running'",shell=True).decode('ascii'))
    getServices = r".*[.]service"

    #All running services
    runningServices = re.findall(getServices,getInfo)

    #Get current time in UTC
    currTime = pytz.utc.localize(datetime.datetime.utcnow().replace(microsecond=0))

    #for loop that finds uptime for each running service
    for i in runningServices:
        getStatus = "systemctl status " + str(i)
        active = r"\s*Active:\s*.*"
        time = r"since\s*[a-zA-Z]*\s*[0-9]*-[0-9]*-[0-9]*\s*[0-9]*:[0-9]*:[0-9]*\s*[a-zA-Z]*;"

        #retreive the status of each service
        try:
            status = str(subprocess.check_output(getStatus,shell=True))
        except:
            print("Error in getRunningServices() in metrics.py: Service call '"+getStatus+"' returned error.")
            
        #parse out the line containing "Active: " and parse out the start time of the service
        findActive = re.findall(active,status)
        findTime = re.findall(time,findActive[0])

        #Format the service start time and put it in UTC
        ufStartTime = parse(findTime[0].replace("since ","").replace(";",""))
        startTime = ufStartTime.astimezone(pytz.timezone("UTC"))

        #Subtract the two values to get the run time of the process and add the service to the dictionary
        uptime = str(currTime - startTime)
        services.update({i:uptime})

    return services


def getNodeID():
    #get the node ID (name)

    #use the 'hostnamectl' command to find the 'Static hostname' of the device and use it as the node id
    hostInfo = str(subprocess.check_output('hostnamectl', shell=True).decode('ascii'))
    pattern = r"Static\s+hostname:.+\n"
    hostName = re.findall(pattern,hostInfo)

    #format the name; remove 'Static hostname'
    ID = hostName[0].replace("Static hostname: ","").replace("\n","")

    #return the node id as a dictionary
    nodeID = {"NodeID":ID}

    return nodeID


def sendMetrics():
    return json.dumps({
        'Timestamp': int(datetime.datetime.utcnow().timestamp() * 1000),  #prints in milliseconds - NOTE May want "human time format"?
        'Node Name': getNodeID(),
        'Uptime': getNodeUptime(),
        'General Info': getGeneralInfo(),
        'Memory Info': getMemInfo(),
        'CPU Info': getCPUInfo(),
        'Disk Info': getDiskInfo(),
        'Services': getRunningServices(),
        'USB Devices': getUSBDevs(),
    })


if __name__ == '__main__':
    for key, val in sorted(json.loads(sendMetrics()).items()):
        print(key)
        print(val)
