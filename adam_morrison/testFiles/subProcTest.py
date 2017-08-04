import subprocess
import re
#a = subprocess.check_output('cat /proc/meminfo', shell=True)
#print a

#b = subprocess.check_output('systemctl show enabled', shell=True)
#print b

getInfo = subprocess.check_output('hostnamectl',shell=True)
print getInfo

print('___________')

#for x in getInfo:
#    print x
check = r"\s*[a-zA-Z]*:\s*.\n|\s*[a-zA-Z]*\s*[a-zA-Z]*:\s*.*\n"
#check = r"[a-zA-Z]*:\s*.\n|[a-zA-Z]*\s*[a-zA-Z]*:\s*.*\n"

#if re.search(check, memInfo[x]):
#memList.append(memInfo[x])
print(re.findall(check,getInfo))

bleh = re.findall(check,getInfo)

for x in bleh:
    print x
