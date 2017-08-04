import re
import subprocess

getInfo = subprocess.check_output('lsusb',shell=True)

#pattern = r"Bus\s*\d+\s*Device\s*\d+:\s*ID.+"

pattern1 = r"Bus\s*\d+\s*Device\s*\d+:"

pattern2 = r"ID\s*[a-zA-Z0-9]+:[a-zA-Z0-9]+"

pattern3 = r"[a-zA-Z0-9]+:[a-zA-Z0-9]+\s*.+"

#devs = re.findall(pattern,getInfo)

devs1 = re.findall(pattern1,getInfo)

devs2 = re.findall(pattern2,getInfo)

devs3 = re.findall(pattern3,getInfo)

#print devs

for x in range(0,7):
    print devs3[x]#devs1[x],devs2[x],devs3[x]
