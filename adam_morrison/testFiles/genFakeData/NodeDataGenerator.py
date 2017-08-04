from Tkinter import *
import subprocess
import datetime
import random
import json
import time
import re

def GUIMain():
    
    def buttonAction():
        print "Generating..."
        timePeriod = getTimePeriod(yrEnt.get(),wkEnt.get(),dayEnt.get(),hrEnt.get(),minEnt.get())
        samplePeriod = getSamplePeriod(yrEnt1.get(),wkEnt1.get(),dayEnt1.get(),hrEnt1.get(),minEnt1.get())
        numNodes = getNumNodes(nodeEnt.get())
        percentFailNodes = getPercentFail(percentEnt.get()) #still need to implement this
        timeRange = getTimeRange(leftEnt.get(),rightEnt.get(),var.get())
        generateNodeData(timePeriod,samplePeriod,numNodes,percentFailNodes,timeRange[0],timeRange[1])
        print "Done."
    
    master = Tk()

    var=StringVar(master)
    var.set("minutes")
    #master.configure(background='light gray')
    #Instantiations
    q1 = Label(master,text="Over what amount of time would you like to generate fake data?")
    q2 = Label(master,text="How often would you like to sample the data?")
    q3 = Label(master,text="How many nodes do you want to test?")
    q4 = Label(master,text="What percent of nodes do you want to be failing?")
    q5 = Label(master,text="What range of times do you want nodes to fail?")

    #Question 1
    q1.grid(row=0,padx=20,pady=20,columnspan=5)

    ##yrChk = Checkbutton(master)
    ##wkChk = Checkbutton(master)
    ##dayChk = Checkbutton(master)
    ##hrChk = Checkbutton(master)
    ##minChk = Checkbutton(master)

    yrEnt = Entry(master, width=4)
    wkEnt = Entry(master,width=4)
    dayEnt = Entry(master,width=4)
    hrEnt = Entry(master,width=4)
    minEnt = Entry(master,width=4)

    yr1Label = Label(master,text="years")
    wk1Label = Label(master,text="weeks")
    day1Label = Label(master,text="days")
    hr1Label = Label(master,text="hours")
    min1Label = Label(master,text="minutes")

    yrEnt.grid(row=1,column=2,sticky=E)
    wkEnt.grid(row=2,column=2,sticky=E)
    dayEnt.grid(row=3,column=2,sticky=E)
    hrEnt.grid(row=4,column=2,sticky=E)
    minEnt.grid(row=5,column=2,sticky=E)

    ##yrChk.grid(row=1,column=1,sticky=E)
    ##wkChk.grid(row=2,column=1,sticky=E)
    ##dayChk.grid(row=3,column=1,sticky=E)
    ##hrChk.grid(row=4,column=1,sticky=E)
    ##minChk.grid(row=5,column=1,sticky=E)

    yr1Label.grid(row=1,column=3,sticky=W)
    wk1Label.grid(row=2,column=3,sticky=W)
    day1Label.grid(row=3,column=3,sticky=W)
    hr1Label.grid(row=4,column=3,sticky=W)
    min1Label.grid(row=5,column=3,sticky=W)

    #Question 2
    q2.grid(row=6,padx=10,pady=10,columnspan=5)

    ##yrChk2 = Checkbutton(master)
    ##wkChk2 = Checkbutton(master)
    ##dayChk2 = Checkbutton(master)
    ##hrChk2 = Checkbutton(master)
    ##minChk2 = Checkbutton(master)

    yrEnt1 = Entry(master, width=4)
    wkEnt1 = Entry(master,width=4)
    dayEnt1 = Entry(master,width=4)
    hrEnt1 = Entry(master,width=4)
    minEnt1 = Entry(master,width=4)

    yrEnt1.grid(row=7,column=2,sticky=E)
    wkEnt1.grid(row=8,column=2,sticky=E)
    dayEnt1.grid(row=9,column=2,sticky=E)
    hrEnt1.grid(row=10,column=2,sticky=E)
    minEnt1.grid(row=11,column=2,sticky=E)

    ##yrChk2.grid(row=7,column=1,sticky=E)
    ##wkChk2.grid(row=8,column=1,sticky=E)
    ##dayChk2.grid(row=9,column=1,sticky=E)
    ##hrChk2.grid(row=10,column=1,sticky=E)
    ##minChk2.grid(row=11,column=1,sticky=E)

    yr2Label = Label(master,text="years")
    wk2Label = Label(master,text="weeks")
    day2Label = Label(master,text="days")
    hr2Label = Label(master,text="hours")
    min2Label = Label(master,text="minutes")

    yr2Label.grid(row=7,column=3,sticky=W)
    wk2Label.grid(row=8,column=3,sticky=W)
    day2Label.grid(row=9,column=3,sticky=W)
    hr2Label.grid(row=10,column=3,sticky=W)
    min2Label.grid(row=11,column=3,sticky=W)

    #Question 3
    q3.grid(row=12,padx=10,pady=10,columnspan=5)

    nodeEnt = Entry(master, width=4)
    nodeLabel = Label(master,text="nodes")

    nodeEnt.grid(row=13, column=2)
    nodeLabel.grid(row=13,column=3,sticky=W)

    #Question 4
    q4.grid(row=14,padx=10,pady=10,columnspan=5)

    percentEnt = Entry(master, width=4)
    percentLabel = Label(master,text="% of nodes")

    percentEnt.grid(row=15, column=2)
    percentLabel.grid(row=15,column=3,sticky=W)

    #Question 5
    q5.grid(row=16,padx=16,pady=10,columnspan=5)

    leftEnt = Entry(master,width=4)
    rightEnt = Entry(master,width=4)
    midLabel = Label(master,text="to")
    menu=OptionMenu(master,var,"years","weeks","days","hours","minutes")

    leftEnt.grid(row=17,column=1,sticky=E)
    rightEnt.grid(row=17,column=3,sticky=W)
    midLabel.grid(row=17,column=2)
    menu.grid(row=17,column=4,sticky=W)


    #Generate button
    genBut = Button(master,text="Generate Data",command=buttonAction)
    genBut.grid(row=118,padx=20,pady=20,columnspan=5)


    #master.geometry("640x480")
    master.title("Node Data Generator")
    master.mainloop()

def generateNodeData(timePeriod,samplePeriod,numNodes,percentFailNodes,fromTime,toTime):
    #generates fake data for a single node using the given parameters
    #looks at data over %timePeriod%, retrieves data from node every %samplePeriod%,
    
    now = datetime.datetime.utcnow()
    addSec = 0
     
    
    #generate the arrays needed
    arrHolder = []
    #print (timePeriod/samplePeriod)-1
    #print timePeriod
    #print samplePeriod

    period = 0
    if (float(timePeriod)/float(samplePeriod)) > timePeriod/samplePeriod:
        period = (timePeriod/samplePeriod)
    else:
        period = (timePeriod/samplePeriod)-1
        
    
    for i in range(0,period):
        arrHolder.append([])
        #print "arrHolder:",i
    #print float(percentFailNodes)/100
    amtFail = float(numNodes)*(float(percentFailNodes)/100)
    #print "Amount Fail:",amtFail
    failArr = [0 for i in range(0,numNodes)]
    failCount = 0
    
    while (failCount < amtFail):
        rnd = random.SystemRandom(int(time.time()))
        randIndex = rnd.randint(-1,numNodes-1)

        if failArr[randIndex] == 0:
            failArr[randIndex] = random.SystemRandom(int(time.time())).randint(fromTime,toTime)
            failCount = failCount + 1
            #print randIndex
            #print failArr[randIndex]
    
    for node in range(0,numNodes):
        #print node
        #generate random fail time
        #rnd = random.SystemRandom(int(time.time()))
        #randNum = rnd.randint(fromTime,toTime)

        #print randNum
        #print fromTime,toTime
        failTime = failArr[node]#randNum
        #print failTime

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
                #print numberCounter
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

def getTimePeriod(years,weeks,days,hours,minutes):
    #returns user-specified time period in seconds
    #print("Over what amount of time would you like to generate fake data?")

    if years == "":
        years = "0"
    if weeks == "":
        weeks = "0"
    if days == "":
        days = "0"
    if hours == "":
        hours = "0"
    if minutes == "":
        minutes = "0"
    timePerYears = int(years)
    timePerWeeks = int(weeks)
    timePerDays = int(days)
    timePerHours = int(hours)
    timePerMins = int(minutes)
    #print "You said",timePerYears,"years,",timePerWeeks,"weeks,",timePerDays,"days,",timePerHours,"hours, and",timePerMins,"minutes"

    #calculate the time period in seconds
    timePeriod = (timePerYears*365*24*60*60)+(timePerWeeks*7*24*60*60)+(timePerDays*24*60*60)+(timePerHours*60*60)+(timePerMins*60)
        
    return timePeriod

def getSamplePeriod(years,weeks,days,hours,minutes):
    #returns user-specified sample rate (how often the nodes are checked/pinged for data) in seconds
    #print("How often would you like to sample the data?")
    
    if years == "":
        years = "0"
    if weeks == "":
        weeks = "0"
    if days == "":
        days = "0"
    if hours == "":
        hours = "0"
    if minutes == "":
        minutes = "0"
    
    samplePerYears = int(years)
    samplePerWeeks = int(weeks)
    samplePerDays = int(days)
    samplePerHours = int(hours)
    samplePerMins = int(minutes)
    #print "You said",samplePerYears,"years,",samplePerWeeks,"weeks,",samplePerDays,"days,",samplePerHours,"hours, and",samplePerMins,"minutes"

    #calculate the sample period in seconds
    samplePeriod = (samplePerYears*365*24*60*60)+(samplePerWeeks*7*24*60*60)+(samplePerDays*24*60*60)+(samplePerHours*60*60)+(samplePerMins*60)

    return samplePeriod

def getNumNodes(nodes):
    #returns user-specified amount of fake nodes to test
    #print("How many nodes do you want to test?")

    if nodes == "":
        nodes = "0"
    numNodes = int(nodes)

    #print "You said you'd like",numNodes,"nodes."

    return numNodes

def getPercentFail(percent):
    #returns user-specified percentage of the nodes that should be having issues/reseting/failing
    #print("What percent of nodes do you want to be failing?")

    if percent == "":
        percent = "0"
    percentFailNodes = int(percent)

    #print "You said you'd like",percentFailNodes,"% of nodes failing."
    return percentFailNodes

def getTimeRange(fromVal,toVal,timeUnit):
    #returns user-specified time range (in seconds) in which a single node could be failing (each node will fail at a certain time between x and y, and that time will be randomly assigned)

    periodList = []
    if timeUnit == "years":
        fromYears = int(fromVal)
        toYears = int(toVal)
        fromWeeks,fromDays,fromHours,fromMins = 0,0,0,0
        toWeeks,toDays,toHours,toMins = 0,0,0,0
    if timeUnit == "weeks":
        fromWeeks = int(fromVal)
        toWeeks = int(toVal)
        fromYears,fromDays,fromHours,fromMins = 0,0,0,0
        toYears,toDays,toHours,toMins = 0,0,0,0
    if timeUnit == "days":
        fromDays = int(fromVal)
        toDays = int(toVal)
        fromYears,fromWeeks,fromHours,fromMins = 0,0,0,0
        toYears,toWeeks,toHours,toMins = 0,0,0,0
    if timeUnit == "hours":
        fromHours = int(fromVal)
        toHours = int(toVal)
        fromYears,fromWeeks,fromDays,fromMins = 0,0,0,0
        toYears,toWeeks,toDays,toMins = 0,0,0,0
    if timeUnit == "minutes":
        fromMins = int(fromVal)
        toMins = int(toVal)
        fromYears,fromWeeks,fromDays,fromHours = 0,0,0,0
        toYears,toWeeks,toDays,toHours = 0,0,0,0
    #print("What range of times do you want nodes to fail?")
    #print("From") 
##    fromYears = int(raw_input("Years:"))
##    fromWeeks = int(raw_input("Weeks:"))
##    fromDays = int(raw_input("Days:"))
##    fromHours = int(raw_input("Hours:"))
##    fromMins = int(raw_input("Minutes:"))
##    #print("to")
##    toYears = int(raw_input("Years:"))
##    toWeeks = int(raw_input("Weeks:"))
##    toDays = int(raw_input("Days:"))
##    toHours = int(raw_input("Hours:"))
##    toMins = int(raw_input("Minutes:"))
    #print "You said from",fromYears,"years,",fromWeeks,"weeks,",fromDays,"days,",fromHours,"hours, and",fromMins,"minutes to",toYears,"years,",toWeeks,"weeks,",toDays,"days,",toHours,"hours, and",toMins,"minutes"

    fromPeriod = (fromYears*365*24*60*60)+(fromWeeks*7*24*60*60)+(fromDays*24*60*60)+(fromHours*60*60)+(fromMins*60)
    toPeriod = (toYears*365*24*60*60)+(toWeeks*7*24*60*60)+(toDays*24*60*60)+(toHours*60*60)+(toMins*60)
    
    periodList.insert(0,fromPeriod)
    periodList.insert(1,toPeriod)
    #print "Perlist 0: ",periodList[0]
    #print "Perlist 1: ",periodList[1]
    
    return periodList

#Main Program

GUIMain()
