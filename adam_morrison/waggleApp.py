from flask import Flask, render_template, Response
import json

from metrics import *

app = Flask(__name__,static_url_path='',template_folder="templates")

@app.route("/")
def home():
    #basic home page - does not need a get function
    return render_template('home.html')

@app.route("/generalInfo")
def generalInfo():
    #pass general info to html template
    
    genInfo = getGeneralInfo()
    nodeUptime = getNodeUptime()
    usbDevs = getUSBDevs()
	
    return render_template('genInfo.html',genInfo=genInfo,upTimeSecs=nodeUptime["UptimeSeconds"],upTimeFormat=nodeUptime["UptimeFormatted"],usbDevs=usbDevs)

#REMOVE THIS EVENTUALLY BUT LEAVE IT IN FOR NOW FOR ZACH
@app.route("/nodeApi")
def sendGenInfo():
    #test function that sends general computer info to Zach's API
    
    getInfo = getGeneralInfo()
    
    with open('/home/adammorr/waggleWebAPI/testFiles/genFakeData/jsonFile.json') as data:
        jsonData = json.load(data)
        
    return Response(json.dumps(jsonData), mimetype='application/json')

@app.route("/memInfo")
def memInfo():
    #pass memory and CPU info to html template
    memoryInfo = getMemInfo()
    cpuInfo = getCPUInfo()
    diskInfo = getDiskInfo()
    diskUsage = diskInfo['CurrentDiskUsage']

    if diskUsage != "test":
        usage = int(diskUsage.replace("%",""))
    else:
        usage = 17
    
    return render_template('memInfo.html', memoryInfo=memoryInfo, cpuInfo=cpuInfo,diskInfo=diskInfo, usage=usage)

@app.route("/services")
def services():
    #pass running services, systemd services, and up time info to html template
    
    runningServList = getRunningServices()
    return render_template('services.html', runningServList=runningServList)

@app.route("/metrics")
def sendMetrics():
    #function that sends data to sendData.py via response/request
    
    nodeID = getNodeID()
    uptime = getNodeUpTime()[0]
        
    jsonData = {}
    jsonData = {'timestamp':float(time.time()),'nodename':nodeID,'uptime':uptime} #time format can be changed if needed

    return Response(json.dumps(jsonData), mimetype='application/json')

if __name__ == "__main__":
    app.run(host='10.31.81.10',port='52117')
    #app.run(host='0.0.0.0',port='52117')
