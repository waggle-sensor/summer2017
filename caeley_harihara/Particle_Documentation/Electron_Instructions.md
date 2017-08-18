# *Electron Instructions*  
## NOTE: If you have never used an electron before, follow the instructions on this link: https://docs.particle.io/guide/getting-started/connect/electron/ to install the Particle CLI

## Connecting to the Electron
*	Plug in the USB cable to power on the electron
*	Plug in external battery
*	Download/open Particle app
*	Press the mode button until the electron blinks dark blue slowly
*	Follow the app’s instructions to add a new device
*	If the Photon is breathing cyan, it’s ready to go!


## Flashing Code to the Electron (Serial)
*	Go to https://build.particle.io/build/new to access Particle’s IDE
*	Write a new application or open a pre-existing application
*	Verify the application by pressing the check mark on the toolbar on the left side of the screen
*	If the code is not properly verified, fix bugs and try to verify again
*	If the code is verified, continue
*	Select the device you want to flash to
    *	Click on the "Devices" icon in the toolbar on the left side of the screen
    *	Select the proper device by starring it
*	Download the firmware from the cloud
    *	Click the “Code” icon in the toolbar
    *	Find the text “Current App” in the gray bar that pops up
    *	Click the cloud icon next to your app’s name (underneath the text that says “Current App”)
    *	Clicking the cloud icon downloads a file called “firmware.bin” to your  machine
*	Put Electron into Listening Mode by holding the mode button for 3 seconds until the LED blinks dark blue 
*	Open the terminal
*	In the terminal, navigate to the folder where “firmware.bin” is stored (will most likely default to being stored in the “Downloads” folder)
*	Enter the command: particle flash --serial firmware.bin
*	If the device is still blinking dark blue, press Enter
*	After flashing different colors (including blinking green and blinking cyan), the led should return to breathing cyan
*	The firmware has now been successfully flashed to the Electron


## Flashing Code to the Electron (Cellular)
*	NOTE: Flashing code with 3G will use at least 20kb of data 
*	Go to https://build.particle.io/build/new to access Particle’s IDE
*	Write a new application or open a pre-existing application
*	Verify the application by pressing the check mark on the toolbar on the left side of the screen
*	If the code is not properly verified, fix bugs and try to verify again
*	If the code is verified, continue
*	Select the device you want to flash to
    *	Click on the "Devices" icon in the toolbar on the left side of the screen
    *	Select the proper device by starring it
*	Flash the application to the Electron by pressing the lightning bolt on the toolbar on the left side of the screen
*	After flashing different colors (including magenta and white), the led should return to breathing cyan
*	The firmware has now been successfully flashed to the Electron


## Viewing Published Events 

*	Used to view events published by “Particle.publish” statements
*	Go to https://console.particle.io/logs to view a log of Photon events
*	To see the same stream of events from the terminal:
    *	Type the following command in the terminal : curl https://api.particle.io/v1/devices/events?access_token={AccessTokenHere}
    *	Replace {AccessTokenHere} with the access token that can be found as follows:
        *	Go to https://build.particle.io
        *	Go to “Settings” by clicking on the gear on the bottom of the toolbar to the left hand side of the screen
        *	The access token will be in the grey box that pops up to the right of the toolbar 
