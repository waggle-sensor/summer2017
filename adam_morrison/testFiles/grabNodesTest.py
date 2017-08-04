import json
import time
import requests
from datetime import datetime

smAddr = "http://10.10.10.131:9000"
cpAddr = "http://10.10.10.172:9000"

counter = 0

while 1:
    #can get the up time one of two ways:
    
    #1: continually ping the node for the up time and use the % operater to do something at a specific time
    #   interval based on the up time (in seconds)
    '''
    if (int(float(cpData['chill_penguin']))) % 60 == 0:
        print "chill_penguin up time:",cpData['chill_penguin']
    if (int(float(smData['spark_mandrill']))) % 60 == 0:
        print "spark_mandrill up time:",smData['spark_mandrill']
    '''
    #2:  only ping the sensor when a specific time (based on real time, not node
    #    node up time) has been reached (% operator against the actual time in seconds?)
    if (int(float(time.time()))) % 10 == 0:
        reqCp = requests.get(cpAddr)
        cpData = reqCp.json()
        print "chill_penguin up time:",cpData['chill_penguin']
    if (int(float(time.time()))) % 10 == 0:
        reqSm = requests.get(smAddr)
        smData = reqSm.json()
        print "spark_mandrill up time:",smData['spark_mandrill']
