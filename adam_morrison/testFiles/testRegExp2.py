from flask import Flask, render_template
import re

memFile = open('/proc/meminfo')
memInfo = memFile.readlines()

for x in range(len(memInfo)):

    check1 = r"[a-zA-Z0-9]+\([a-zA-Z0-9]+\):\s*[0-9]|[a-zA-Z0-9]+:\s*[0-9]"
    print"------------------"
    if re.search(check1, memInfo[x]):
        print memInfo[x]
        print (x)
        print ("Matches")
    else:
        print("v_____________________v")
        print memInfo[x]
        print(x)
        print("Does Not Match")
        print("^_____________________^")
