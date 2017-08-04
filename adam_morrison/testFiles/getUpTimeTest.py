import subprocess

getInfo = subprocess.check_output('cat /proc/uptime',shell=True)
print getInfo
