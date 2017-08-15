# *Water Level Sensor*
## Part I. General Overview
### What is the sensor and what does it do?

The Water Level Sensor from RobotDyn detects the presence of water (i.e. when water touches the metal plates on the sensor), and is therefore used as a proxy.
This will be finalized once the test results are in

### Datasheet

No data sheet currently exists for the water level sensor
### Connection Images
The following image describes how to connect PMS3003 to a Particle **Photon** board. Both sensors share the same connection diagram. Additionally, the **Electron** Particle board and Water Level Sensor connection diagram is identical to the Photon connection diagram. For more information on how to configure the Electron, [click here](https://github.com/charihara/Experimental_Sensors/blob/master/Electron_Instructions.md).


<img src="https://github.com/JordanFleming/sensor_documentation/blob/master/Water_Level_Sensor/images/WaterLevelSensor_B_ConnectionDiagram.jpg?raw=true" width="650" height="400">

<img src="https://github.com/JordanFleming/sensor_documentation/blob/master/Water_Level_Sensor/images/WaterLevelSensor_R_ConnectionDiagram.jpg?raw=true" width="650" height="400">

### Working Logic / Functionality
#### Output
* Type: Analog
* Default baud rate: 9600 bps

## Part II. Waggle Specific
### Application
#### How does the sensor work with Photon and Particle I/O Cloud?
The Water Level Sensor transmits a resistance through the analog pin on the Particle Photon.. The [source code posted below](#particle) publishes the data as a live stream of events to the Particle cloud (click [here to visit the Particle cloud event console](https://console.particle.io/events)). 

The data is not stored on the Particle cloud, you must purchase storage space through Particle or save the data to a text file -- or something similar -- in order to retain information. The Particle Photon communicates with the Particle cloud via WiFi. The data can be pushed from the Particle cloud and into Beehive dev ([for more documentation on this process, click here](#beehive)). 

#### How do I setup a Particle Photon?
[Documentation detailing how to setup the Particle Photon can be found here.](https://github.com/charihara/Experimental_Sensors/blob/master/Photon_Instructions.md)

### Source Code on particle.io <a name="particle"></a>
```C   
#define Water_Level_Sensor A0 //Sensor output

int water_level_counts;

void setup() 
{
    pinMode(Water_Level_Sensor, INPUT);
}

void loop() 
{

    water_level_counts = 0x00;
    for(int i = 0x00; i < 16; i++)
    {
        water_level_counts = water_level_counts + (analogRead(Water_Level_Sensor));
        delay(100);
    }
    water_level_counts = water_level_counts >> 2;
    Particle.publish("Water_Level", String(water_level_counts), PRIVATE);
    
}

```    
    
### Particle Data Interface with Beehive dev <a name="beehive"></a>

[Particle to Beehive dev source code](https://github.com/JordanFleming/sensor_documentation/blob/master/Particle_to_Beehive_plugin)
### Waggle-space ID
[Sensor ID Table](https://github.com/JordanFleming/sensor_documentation/blob/master/Sensor_IDs.md)
