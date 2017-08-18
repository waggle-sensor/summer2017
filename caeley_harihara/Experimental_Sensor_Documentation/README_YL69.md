# *YL-69 Sensor*
## Part I. General Overview
### What is the YL-69?

  * Detects the humidity of the soil
  * Requires a 5V power supply
  * Type: analog
  * Output voltage decreases as the soil moisture increases

### Tutorial
[YL-69 Tutorial](https://github.com/charihara/Experimental_Sensors/blob/master/Datasheets/YL69_Guide.pdf)

[Original Source](https://randomnerdtutorials.com/guide-for-soil-moisture-sensor-yl-69-or-hl-69-with-the-arduino/)
### Connection Images
![image of YL-69 connection](https://github.com/charihara/Experimental_Sensors/blob/master/Images/YL69_Connection_1.JPG)

The YL-69 sensor is hooked up as a voltage divider. For more information about voltage dividers and examples, see:

[Voltage Divider Explanation.](https://en.wikipedia.org/wiki/Voltage_divider)

[Voltage Divider Example (Ohm Meter).](http://www.circuitbasics.com/arduino-ohm-meter/)

[Voltage Divider Example (FSR).](https://learn.adafruit.com/force-sensitive-resistor-fsr/using-an-fsr)
### Working Logic / Functionality
#### Output

  * Type: analog
  * Output voltage decreases when the soil is wet
  * Output voltage increases when the soil is dry

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
