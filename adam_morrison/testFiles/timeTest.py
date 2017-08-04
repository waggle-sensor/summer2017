import time
from datetime import datetime, timedelta
#oldTime = 15:33:43
#currentTime = time.time()

#elapsedTime = currentTime - oldTime
#print(elapsedTime)
print(time.time())

time1 = datetime("Mon 2017-06-12 15:33:43 CDT")
time2 = datetime("Mon 2017-06-12 15:37:43 CDT")
timedelta = datetime.datetime.strptime(time1, datetimeFormat) - datetime.datetime.strptime(time2,datetimeFormat)
