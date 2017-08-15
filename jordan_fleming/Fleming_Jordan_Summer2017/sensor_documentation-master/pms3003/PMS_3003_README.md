# *PMS3003 Sensor*
## Part I. General Overview
### What is the sensor and what does it do?

The Plantower PMS3003 is a particle sensor that measures particulate matter in the air uisng laser scattering. The sensor is sensitive enough to detect 0.3 um particles.

### Datasheet
[PMS 3003 Datasheet](https://github.com/JordanFleming/sensor_documentation/blob/master/datasheets/PMS3003_Datasheet.pdf)
### Connection Images
<img src="https://github.com/JordanFleming/sensor_documentation/blob/master/pms3003/images/PMS3003_pin_out.jpg?raw=true" width="600" height="350">

The following image describes how to connect PMS3003 to a Particle **Photon** board. Additionally, the **Electron** Particle board and Water Level Sensor connection diagram is identical to the Photon connection diagram. For more information on how to configure the Electron, [click here](https://github.com/charihara/Experimental_Sensors/blob/master/Electron_Instructions.md).


<img src="https://github.com/JordanFleming/sensor_documentation/blob/master/pms3003/images/connection_diagram_pms30003.png?raw=true" width="650" height="500">

### Working Logic / Functionality
#### Output
* Type: UART
* Default baud rate: 9600 bps
  * Parity: None
  * Stop bit: 1 bit
* Length: 24 bytes
  <img src="https://github.com/JordanFleming/sensor_documentation/blob/master/pms3003/images/bit_parsing.jpg?raw=true">

## Part II. Waggle Specific
### Application
#### How does the sensor work with Photon and Particle I/O Cloud?
PMS3003 transmits a 24 byte hex string through the serial port on the Particle Photon. The source code posted below publishes the data as a live stream of events to the Particle cloud (click [here to visit the Particle cloud event console](https://console.particle.io/events)). 

The data is not stored on the Particle cloud, you must purchase storage space through Particle or save the data to a text file -- or something similar -- in order to retain information. The Particle Photon communicates with the Particle cloud via WiFi. The data can be pushed from the Particle cloud and into Beehive dev ([for more documentation on this process, click here](#beehive)). 

From here the data is parsed in Beehive dev to retrieve human readable particulate matter concentrations in ug/m^3.

#### How do I setup a Particle Photon?
[Documentation detailing how to setup the Particle Photon can be found here.](https://github.com/charihara/Experimental_Sensors/blob/master/Photon_Instructions.md)

### Source Code from particle.io
```C   
    #include "Particle.h"

    #define PMS7003 0x01
    // #define PMS3003 0x02

    #ifdef PMS7003
    #define LENG 32
    #endif 

    #ifdef PMS3003
    #define LENG 24
    #endif 

    char buf[LENG + 2];
    int data_CRC = 0x00;




      void setup()
      {
       Serial1.begin(9600);   //use serial0
      }

      void loop()
      {
    
    if (Serial1.available() > 0)
    
    {
        
        //Particle.publish("RSG-1", String(Serial.read()), PRIVATE);
        
       if (Serial1.read() == 0x42)
            
        {
            
            Serial1.readBytes(buf,LENG-1);
            if(buf[0] == 0x4d)
            {
                data_CRC = 0x42;
                for ( int i = 0x00; i < LENG -3 ; i ++)
                {
                    data_CRC = data_CRC + buf[i] ; 
                }
                
                if ( data_CRC == (( buf[LENG - 3] << 8 ) + buf[LENG - 2]))
                {
                    String data_send;
                    for (unsigned char i = 0x00; i < LENG; i++)
                    {
                        if (buf[i] < 0x10)
                        {
                            data_send = data_send + '0';    
                        }
                        
                        data_send = data_send + String(buf[i],HEX);
                    }
                    
                    Particle.publish("PMS7003", data_send, PRIVATE);
                    
                }
            }
        }
        
        
    }
    
    delay(500);
    
    }
```    
    
### Particle Data Interface with Beehive dev <a name="beehive"></a>

[Particle to Beehive dev source code](https://github.com/JordanFleming/sensor_documentation/blob/master/Particle_to_Beehive_plugin)
### Waggle-space ID
[Sensor ID Table](https://github.com/JordanFleming/sensor_documentation/blob/master/Sensor_IDs.md)
### Data Structure
