from flask import Flask, render_template, Response
from dateutil.parser import parse
from datetime import datetime

import subprocess
import datetime
import json
import time
import pytz
import re

name = ""
typeOf = ""
used = ""
free = ""

getInfo = subprocess.check_output('~/waggleWebAPI/detectDiskDevices.sh', shell=True)

print getInfo

pattern = r".*memory card not recognized.*"
if (re.search(pattern, getInfo)):
    name = ["test","test2"]
    typeOf = ["test","test2"]
    used = ["test","test2"]
    free = ["test","test2"]
else:
    name = [re.findall(r"CURRENT_DISK_DEVICE_NAME=.*",getInfo),re.findall(r"OTHER_DISK_DEVICE_NAME=.*",getInfo)]
    typeOf = [re.findall(r"CURRENT_DISK_DEVICE_TYPE=.*",getInfo),re.findall(r"OTHER_DISK_DEVICE_TYPE=.*",getInfo)]
    used = ["17%","17%"]
    free = ["83%","83%"]

diskInfo = [name,typeOf,used,free]
print diskInfo
#return diskInfo

