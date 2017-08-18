# *DS18B20 Sensor*
## Part I. General Overview
### What is the DS18B20?

  * 1-Wire Digital Thermometer
  * Measures Temperatures from -55°C to +125°C
  * Must be used with a pull up resistor with a value of around 4.7 kΩ
  * Power supply range: 3.0 V to 5.5 V
  * Requires only 1 port pin for communication

### Datasheet
[DS18B20 Datasheet](https://github.com/charihara/Experimental_Sensors/blob/master/Datasheets/DS18B20_Data_Sheet.pdf)

### Connection Images
![image of DS18B20 connection](https://github.com/charihara/Experimental_Sensors/blob/master/Images/DS18B20_Connection.JPG)

### Working Logic / Functionality
#### Output

  * Thermometer resolution is user-selectable from 9 to 12 bits
  * Converts temperatues to 12-bit digital word in 750 ms

## Part II. Waggle Specific
### Application
#### How does my sensor work with a Particle Photon?
[Documentation detailing how to setup and read data from the Particle Photon can be found here.](https://github.com/charihara/Experimental_Sensors/blob/master/Photon_Instructions.md)
#### How does my sensor work with a Particle Electron?
[Documentation detailing how to setup and read data from the Particle Electron can be found here.](https://github.com/charihara/Experimental_Sensors/blob/master/Electron_Instructions.md)

### Source Code from particle.io

```C 
int rainPin = A0;

void setup() {
    
  pinMode(rainPin, INPUT);

}

void loop() {
 // read the input on analog pin 0:
  int sensorValue = analogRead(rainPin);
  Particle.publish("YL-69", String(sensorValue), PRIVATE);
  delay(60000);

}
```
### Particle Data Interface with Beehive dev <a name="beehive"></a>
[Particle to Beehive dev source code](https://github.com/JordanFleming/sensor_documentation/blob/master/Particle_to_Beehive_plugin)
### Waggle-space ID
[Sensor ID Table](https://github.com/JordanFleming/sensor_documentation/blob/master/Sensor_IDs.md)
