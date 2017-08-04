from datetime import datetime
from dateutil.parser import parse
import pytz
import datetime

#UTC time is used since one does not have to worry about Daylight Savings Time
#and the times are standardized so that the run time can be correctly calculated

#Get current time in UTC
ufCurrTime = datetime.datetime.utcnow()

currTime = pytz.utc.localize(datetime.datetime.utcnow().replace(microsecond=0))

#Format the service start time (uses arbitrary start time for now)
ufStartTime = parse("Tue 2017-06-13 08:45:49 CDT")
startTime = ufStartTime.astimezone(pytz.timezone("UTC"))

#Subtract the two values to get the run time of the process

print "The current time is: "
print currTime
print "_____________________________________"
print "The time that the process started is: "
print startTime
print "_____________________________________"
print "The run time, therfore, is: "
print currTime - startTime




