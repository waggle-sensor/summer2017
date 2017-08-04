import subprocess
import re

getHostName = subprocess.check_output('hostnamectl', shell=True)
findPattern = r"\s*[a-zA-Z]*:\s*.\n|\s*[a-zA-Z]*\s*[a-zA-Z]*:\s*.*\n"

genInfoList = re.findall(findPattern,getHostName)

print dict(x.split(':') for x in genInfoList)

theDict = dict(x.split(':') for x in genInfoList)

for x,y in theDict.iteritems():
    print x,":", y
