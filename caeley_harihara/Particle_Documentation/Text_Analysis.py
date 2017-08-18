file = open("Data.txt")

line = file.readline()
# print(line)
timestamp,ID,data = [f.strip() for f in line.split(" ")]
# print(timestamp)
# print(ID)
# print(data)
date,time = [f.strip() for f in line.split("T")]
# print(date)
# print(time)

redFile = open(str('RED_Water_Sensor_'+ date +'.txt'), 'a')
blackFile = open(str('BLACK_Water_Sensor_'+ date +'.txt'), 'a')
soilMoistureFile = open(str('Soil_Moisture_Counts_'+ date +'.txt'), 'a')

while True:
   line = file.readline().strip()
   # print(line)h
   if not line:
       print("done")
       break
   timestamp,ID,data = line.split(" ")
   date,time = [f.strip() for f in timestamp.split("T")]
   timeKeep, timeDiscard = time.split(".")
   # time = str(time)
   # print(timestamp)
   # print(ID)
   # print(data)
   # print(date)
   # print(time)
   if ID == "RED_Water_Sensor":
       redFile.write(str(date) + " " + str(timeKeep) + " " + str(ID) + " " + str(data))
       print(str(timeKeep) + "\n")
       redFile.write("\n")
   if ID == "BLACK_Water_Sensor":
       blackFile.write(str(date) + " " + str(timeKeep) + " " + str(ID) + " " + str(data))
       blackFile.write("\n")
   if ID == "Soil_Moisture_Counts":
       soilMoistureFile.write(str(date) + " " + str(timeKeep) + " " + str(ID) + " " + str(data))
       soilMoistureFile.write("\n")

file.close()
