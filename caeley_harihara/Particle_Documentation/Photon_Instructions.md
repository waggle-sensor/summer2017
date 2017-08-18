# *Photon Instructions*  
## NOTE: If you have never used a photon before, follow the instructions on this link: https://docs.particle.io/guide/getting-started/connect/photon/ to install the Particle CLI 

## Connect to the Photon

*	Plug in the USB cable to power on the Photon
*	Download/open Particle app
*	Press the setup button until the photon blinks dark blue slowly
*	If the device has previously been connected, hold down the setup button for ~15 seconds until the led blinks dark blue rapidly
*	Follow the app’s instructions to add a new device 
*	If the Photon is breathing cyan, it’s ready to go!

## Flashing Code to the Photon

*	Go to https://build.particle.io/build/new to access Particle’s IDE
*	Write a new application or open a pre-existing application
*	Verify the application by pressing the check mark on the toolbar on the left side of the screen 
  *	If the code is not properly verified, fix bugs and try to verify again
  *	If the code is verified, continue
* Select the device you want to flash to
  * Click on the "Devices" icon in the toolbar on the left side of the screen
  * Select the proper device by starring it
*	Flash the application to the photon by pressing the lightning bolt on the toolbar on the left side of the screen
*	After flashing different colors (including magenta and white), the led should return to breathing cyan 
*	The firmware has now been successfully flashed to the Photon  

## Viewing Published Events 

*	Used to view events published by “Particle.publish” statements
*	Go to https://console.particle.io/logs to view a log of Photon events
*	To see the same stream of events from the terminal:
    *	Type the following command in the terminal : curl https://api.particle.io/v1/devices/events?access_token={AccessTokenHere}
    *	Replace {AccessTokenHere} with the access token that can be found as follows:
        *	Go to https://build.particle.io
        *	Go to “Settings” by clicking on the gear on the bottom of the toolbar to the left hand side of the screen
        *	The access token will be in the grey box that pops up to the right of the toolbar 
