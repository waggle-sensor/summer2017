from flask import Flask, render_template
import re

memFile = open('/proc/meminfo')
memInfo = memFile.readlines()

cpuFile = open('/proc/cpuinfo')
cpuInfo = [line.split('\n') for line in cpuFile.readlines()]



num = 0
noMatch = 0
for x in range(len(memInfo)):

    check1 = r"[a-zA-Z0-9]+\([a-zA-Z0-9]+\):\s*[0-9]"
    #check = r"[a-zA-Z0-9]+\([a-zA-Z0-9]+\):\s*[0-9]\s*[a-zA-Z0-9]"
    #check = r"[a-zA-Z0-9]+:\s*[0-9]\s*[a-zA-Z0-9]"
    check2 = r"[a-zA-Z0-9]+:\s*[0-9]"
    print"------------------"
    if re.search(check1, memInfo[x]):
        print memInfo[x]
        print (x)
        print ("Matches")
    elif re.search(check2, memInfo[x]):
        print memInfo[x]
        print (x)
        print ("Matches")
    else:
        print("v_____________________v")
        print memInfo[x]
        print(x)
        print("Does Not Match")
        print("^_____________________^")
        noMatch = noMatch + 1
    num = num + 1
print("Number of non-matches: " + str(noMatch))
