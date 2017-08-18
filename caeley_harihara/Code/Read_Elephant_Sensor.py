import serial
import time
import datetime


dateString = str(datetime.date.today())


timeout = None
# Identifies the sensor
ser = serial.Serial(
    port='/dev/calibSense',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.flushInput()
ser.flushOutput()

# Reads in each line of the sensor's data to check if it has the right format
def readLines():
    while True:
        line = ser.readline().decode()
        if '=' in line:
            yield [f.strip() for f in line.split("=")]

# Instance variables
count = 0
tempSum = 0.0
humSum = 0.0

fileToSave = open(str('/root/Python/'+time.strftime("%d-%m-%y")+'.txt'), 'a')
utc_datetime = datetime.datetime.utcnow()
currentDate = utc_datetime.strftime("%d-%m-%y")

while True:
    time.sleep(0.01)
    # characterization: Temp or Humidity , number: associated value
    for characterization,numberString in readLines():
        number = float(numberString)

    # Change what file is saved to as the day changes
        utc_datetime = datetime.datetime.utcnow()
        if currentDate != utc_datetime.strftime("%d-%m-%y"):
            fileToSave.close()
            currentDate=utc_datetime.strftime("%d-%m-%y")
            fileToSave = open('/root/Python/'+currentDate + '.txt', 'a')
            count = 0
            tempSum = 0.0
            humSum = 0.0

        if count == 30:
            # nowTime: time when half of the 30 samples have been taken
            nowTime = int(time.time()) - 15

        if characterization == "Humidity":
            humSum += number

        elif characterization == "Temperature":
            tempSum += number

        count += 1

        if count == 60:
            # Calculates the average temp and humidity over 30 seconds
            avgTemp = tempSum/30.0
            avgHum = humSum/30.0
            fileToSave.write('Time: %s, Average Temperature: %.2f, Average Humidity: %.2f' % (nowTime, avgTemp, avgHum))
            fileToSave.write("\n")
            fileToSave.flush()
            print(time.asctime())
            # Resets instance variables
            count = 0
            tempSum = 0.0
            humSum = 0.0
            break
