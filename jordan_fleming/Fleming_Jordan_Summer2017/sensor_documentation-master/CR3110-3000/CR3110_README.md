# *CR3110-3000 Sensor*
## Part I. General Overview
### What is the sensor and what does it do?

The CR Magnetics CR3110-3000 is a split core current transformer that measures current flowing through a single cord. [Click here for more information on current sensing theory.](http://www.nktechnologies.com/engineering-resources/current-sensing-theory/)

### Datasheet
[CR3110-3000 Datasheet](https://github.com/JordanFleming/sensor_documentation/blob/master/datasheets/CR3110_datasheet.jpg)
### Connection Images
The following image describes how to connect CR3110-3000 to a Particle **Photon** board. Additionally, the **Electron** Particle board and CR31100-3000 connection diagram is identical to the Photon connection diagram. For more information on how to configure the Electron, [click here](https://github.com/charihara/Experimental_Sensors/blob/master/Electron_Instructions.md).


<img src="https://github.com/JordanFleming/sensor_documentation/blob/master/CR3110-3000/images/CR3110_full_connection_diagram.png?raw=true">

### Working Logic / Functionality
#### Output
* Type: Voltage

## Part II. Waggle Specific
### Application
#### How does the sensor work with Photon and Particle I/O Cloud?
CR3110-3000 transmits data through an analog pin on the Particle Photon. The sensor outputs voltage which must be converted into current values. The sensor outputs AC voltage which must be turned into DC voltage according to the input specification for the Particle Photon. A full wave bridge rectifier was used to add a DC bias; [click here for a deeper look at building a full wave bridge rectifier](http://www.electronics-tutorials.ws/diode/diode_6.html). The full wave bridge rectifier circuit is pictured below.

<img src="https://github.com/JordanFleming/sensor_documentation/blob/master/CR3110-3000/images/fullwave_bridge_rectifier.png?raw=true" width="600" height="300">

The following diagram describes the characterization of the sensor. This means...

[insert image of characterization plot]

The source code posted below publishes the data as a live stream of events to the Particle cloud (click [here to visit the Particle cloud event console](https://console.particle.io/events)). The data is not stored on the Particle cloud, you must purchase storage space through Particle or save the data to a text file -- or something similar -- in order to retain information. The Particle Photon communicates with the Particle cloud via WiFi. The data can be pushed from the Particle cloud and into Beehive dev ([for more documentation on this process, click here](#beehive)).

#### How do I setup a Particle Photon?
[Documentation detailing how to setup the Particle Photon can be found here.](https://github.com/charihara/Experimental_Sensors/blob/master/Photon_Instructions.md)

### Source Code on particle.io
```C
    #include "Particle.h"
    unsigned int current_value_analog;
    #define Device_Current_Threshold 30 //in A/D Values
    void setup()
    {
    
    }

    void loop()
    {
    current_value_analog = analogRead(A0);
    
    if (current_value_analog > Device_Current_Threshold)
    {
        Particle.publish("Power_Sensor", "Device_ON", PRIVATE);
    }
    else
    {
        Particle.publish("Power_Sensor", "Device_OFF", PRIVATE);
    }
    delay(1000);
    Particle.publish("CR3110-3000", String(current_value_analog), PRIVATE);
    delay(2000);
    }
    
 ```
    
    
### Particle Data Interface with Beehive dev <a name="beehive"></a>

[Particle to Beehive dev source code](https://github.com/JordanFleming/sensor_documentation/blob/master/Particle_to_Beehive_plugin)
### Waggle-space ID
[Sensor ID Table](https://github.com/JordanFleming/sensor_documentation/blob/master/Sensor_IDs.md)

