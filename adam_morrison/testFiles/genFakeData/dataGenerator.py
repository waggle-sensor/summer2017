import subprocess
import json
import time
import re

import datetime
import random

import time


def generateNodeData(timePeriod, samplePeriod,numNodes,fromTime,toTime):

    now = datetime.datetime.utcnow()
    addSec = 0
    #generates fake data for a single node using the given parameters
    #looks at data over %timePeriod%, retrieves data from node every %samplePeriod%, 
    '''
    failingTimeInHours = 2 #fails every x hours !!!!NEED TO REPLACE THIS AT SOME POINT!!!!!

    counter = 0
    upTime = 0
    pingCounter = 0
    numberCounter = 0 #for debugging

    #generating fake node data
    #while loop that runs the simulation for the specified time period
    while counter < timePeriod:

        #if statement that checks wether it is time to grab the node uptime or not
        #if it is time, the node uptime is printed and the pingCounter is reset
        if (pingCounter == samplePeriod):
            numberCounter = numberCounter + 1 #debugging
            #print numberCounter,"Node 1, Uptime =",upTime
            print json.dumps({str(now + datetime.timedelta(seconds=addSec)):upTime})
            addSec = addSec + samplePeriod
            pingCounter = 0

        #if statement that resets the uptime if the failing time has been reached
        #if no failing time is specified, the up time rises continuously (the node is therefore not failing)
        if (upTime < failingTimeInHours*60*60) | (failingTimeInHours == 0):
            upTime = upTime + 1
        else:
            upTime = 1

        #increase the counter for checking the node uptime
        pingCounter = pingCounter + 1
        #increase the time period counter so that the simulation can end after the given time period
        counter = counter + 1

    #print the counter to make sure that the time period has been reached (debugging)
    print counter
    '''
    #generate the arrays needed
    arrHolder = []
    for i in range(0,(timePeriod/samplePeriod)-1):
        arrHolder.append([])
    
    for node in range(0,numNodes):
        #print node
        #generate random fail time
        rnd = random.SystemRandom(int(time.time()))
        randNum = rnd.randint(fromTime,toTime)

        #print randNum
        #print fromTime,toTime
        failTime = randNum

        counter = 0
        upTime = 0
        pingCounter = 0
        numberCounter = 0 

        #generating fake node data
        #while loop that runs the simulation for the specified time period
        while counter < timePeriod:

            #if statement that checks wether it is time to grab the node uptime or not
            #if it is time, the node uptime is printed and the pingCounter is reset
            if (pingCounter == samplePeriod):
                
                #print numberCounter,"Node 1, Uptime =",upTime
                #print json.dumps({str(now + datetime.timedelta(seconds=addSec)):upTime})
                #for arr in arrHolder:
                arrHolder[numberCounter].insert(node,upTime)#.insert(node,"Node"+str(node)+"="+str(upTime))
                numberCounter = numberCounter + 1
                    #print node,upTime
                pingCounter = 0

            #if statement that resets the uptime if the failing time has been reached
            #if no failing time is specified, the up time rises continuously (the node is therefore not failing)
            if (upTime < failTime) | (failTime == 0):
                upTime = upTime + 1
            else:
                upTime = 1

            #increase the counter for checking the node uptime
            pingCounter = pingCounter + 1
            #increase the time period counter so that the simulation can end after the given time period
            counter = counter + 1

        #print the counter to make sure that the time period has been reached (debugging)
        #print counter

    jsonDict = {}
    for arr in arrHolder:
        jsonDict.update({str(time.time() + addSec):arr})#({str(datetime.datetime.utcnow() + datetime.timedelta(seconds=addSec)):arr})
        addSec = addSec + samplePeriod
    #print jsonDict

    with open('jsonFile.json', 'w') as outfile:  
        json.dump(jsonDict, outfile)
    
    #jsonFile=open("jsonText.txt","w")
    #jsonFile.write(str(jsonDict))

def getTimePeriod():
    #returns user-specified time period in seconds
    print("Over what amount of time would you like to generate fake data?")

    timePerYears = int(raw_input("Years:"))
    timePerWeeks = int(raw_input("Weeks:"))
    timePerDays = int(raw_input("Days:"))
    timePerHours = int(raw_input("Hours:"))
    timePerMins = int(raw_input("Minutes:"))
    print "You said",timePerYears,"years,",timePerWeeks,"weeks,",timePerDays,"days,",timePerHours,"hours, and",timePerMins,"minutes"

    #calculate the time period in seconds
    timePeriod = (timePerYears*365*24*60*60)+(timePerWeeks*7*24*60*60)+(timePerDays*24*60*60)+(timePerHours*60*60)+(timePerMins*60)
        
    return timePeriod

def getSamplePeriod():
    #returns user-specified sample rate (how often the nodes are checked/pinged for data) in seconds
    print("How often would you like to sample the data?")

    samplePerYears = int(raw_input("Years:"))
    samplePerWeeks = int(raw_input("Weeks:"))
    samplePerDays = int(raw_input("Days:"))
    samplePerHours = int(raw_input("Hours:"))
    samplePerMins = int(raw_input("Minutes:"))
    print "You said",samplePerYears,"years,",samplePerWeeks,"weeks,",samplePerDays,"days,",samplePerHours,"hours, and",samplePerMins,"minutes"

    #calculate the sample period in seconds
    samplePeriod = (samplePerYears*365*24*60*60)+(samplePerWeeks*7*24*60*60)+(samplePerDays*24*60*60)+(samplePerHours*60*60)+(samplePerMins*60)

    return samplePeriod


def getNumNodes():
    #returns user-specified amount of fake nodes to test
    print("How many nodes do you want to test?")

    numNodes = int(raw_input("Number of nodes: "))

    print "You said you'd like",numNodes,"nodes."

    return numNodes

def getPercentFail():
    #returns user-specified percentage of the nodes that should be having issues/reseting/failing
    print("What percent of nodes do you want to be failing?")
    percentFailNodes = raw_input("Percent of nodes failing: ")

    print "You said you'd like",percentFailNodes,"% of nodes failing."
    return percentFailNodes

def getTimeRange():
    #returns user-specified time range (in seconds) in which a single node could be failing (each node will fail at a certain time between x and y, and that time will be randomly assigned)

    periodList = []
    
    print("What range of times do you want nodes to fail?")
    print("From")
    fromYears = int(raw_input("Years:"))
    fromWeeks = int(raw_input("Weeks:"))
    fromDays = int(raw_input("Days:"))
    fromHours = int(raw_input("Hours:"))
    fromMins = int(raw_input("Minutes:"))
    print("to")
    toYears = int(raw_input("Years:"))
    toWeeks = int(raw_input("Weeks:"))
    toDays = int(raw_input("Days:"))
    toHours = int(raw_input("Hours:"))
    toMins = int(raw_input("Minutes:"))
    print "You said from",fromYears,"years,",fromWeeks,"weeks,",fromDays,"days,",fromHours,"hours, and",fromMins,"minutes to",toYears,"years,",toWeeks,"weeks,",toDays,"days,",toHours,"hours, and",toMins,"minutes"

    fromPeriod = (fromYears*365*24*60*60)+(fromWeeks*7*24*60*60)+(fromDays*24*60*60)+(fromHours*60*60)+(fromMins*60)
    toPeriod = (toYears*365*24*60*60)+(toWeeks*7*24*60*60)+(toDays*24*60*60)+(toHours*60*60)+(toMins*60)
    
    periodList.insert(0,fromPeriod)
    periodList.insert(1,toPeriod)
    #print "Perlist 0: ",periodList[0]
    #print "Perlist 1: ",periodList[1]
    
    return periodList

timePeriod = getTimePeriod()
samplePeriod = getSamplePeriod()
numNodes = getNumNodes()
#percentFailNodes = getPercentFail() #still need to implement this
timeRange = getTimeRange()
 
generateNodeData(timePeriod,samplePeriod,numNodes,timeRange[0],timeRange[1])

