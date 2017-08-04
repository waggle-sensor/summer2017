import subprocess
import time
import re


upTimeCmd = subprocess.check_output('cat /proc/uptime', shell=True)

pattern = r"\d*\.\d*\s+"

#print upTimeCmd

upTime = re.findall(pattern,upTimeCmd)

#print upTime
print upTime[0]

