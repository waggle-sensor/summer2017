# waggleWebAPI README

## Overview of Directories/Files

* **beehive-dev-node-0000-code** dir: contains files for connecting to beehive (files written by Bill Catino)
* **presentationMaterial** dir: contains further information on this API and my research paper from summer 2017
* **static** dir: Flask directory containing the .ico image for the local web app and the CSS style sheet
* **templates** dir: Flask directory containing the html page templates for the local web app
* **testFiles** dir: contains files that were used in the creation of the web app; for backup purposes
* **testFiles/genFakeData** dir: contains files used in creation of fake data; for backup purposes
* **detectDiskDevices.sh** file: script that detects which media the node is booted from (file written by Peter Lane)
* **install.sh** file: script that can be run in order to install this system on a Node (NOTE: incomplete)
* **metrics.py** file: python module containing functions to get metrics from nodes
* **send-node-metrics.service** file: service that sends the node data to the RabbitMQ node-metrics queue (to be placed in /etc/systemd/system)
* **sendData.py** file: pushes node data to beehive (contains code written by Bill Catino)
* **start-web-app.service** file: service that starts the local web app on the node (to be placed in /etc/systemd/system)
* **waggleApp.py** file: creates the local web app and sends node data to sendData

## Overview of waggleWebAPI
This directory contains files and other directories neccesary to run the Waggle Node Metrics API. This system runs on a Node and has three main parts: data aggregation, data transmittance, and the web app. The API can aggregate various metrics from a Node and package them in a Python dictionary in JSON format. It can also send this data to RabbitMQ for holding, where another team member's code would grab it and store it in the beehive-dev database. The final part is a local web view of the aggregated metrics using Flask in Python, HTML, CSS, and a bit of JavaScript. Please see the presentationMaterial directory for further explanation on this API.

**Note:** The beehive-dev-node-0000-code directory usually contains cert and other files that give it access to RabbitMQ. However, these files are not uploaded for security reasons, so new certificates would need to be generated and placed in this directory in order for the data transmittance part of the API to work correctly.

## Installation Notes
In order to install this API on a Node, there are several steps that need to be taken before the system will work correctly. As mentioned above, certain permissions and certificates may be missing from the beehive-dev-node-0000-code directory due to security reasons when uploading to github. The first step would be to re-generate keys and permissions and place them in this directory (according to the names and locations that the 'sendData.py' file expects).

### Installation Steps
**Note:** Some commands may require super user `sudo` at beginning

1. The first step in installation is to run the following two commands: `apt-get update` to update the OS and 
   `apt-get install python-pika python-requests git python-dateutil curl python-pip` to install git, curl, and the necessary    python modules.

2. Run each of these commands:
   `export LC_ALL="en_US.UTF-8"`
   `export LC_CTYPE="en_US.UTF-8"`
   `dpkg-reconfigure locales`
   to change locales so that the code will run correctly.
   When given a GUI with a list of locales when running the `dpkg-reconfigure locales` command, select "en_US.UTF-8 UTF-8"

3. Then, create a directory where you want the API to be installed by running `mkdir` followed by the directory name

4. Run `git clone` followed by the full URL of this GitHub directory inside the directory created in the previous step to        download all files from GitHub.

5. Next, run each of these commands to finish installing the necessary python modules
   `pip install --upgrade pip`,`pip install pytz`, and `pip install flask` 
   
6. Run `cp /PATH_TO_DIRECTPRY/send-node-metrics.service /etc/systemd/system` and 
   `cp /PATH_TO_DIRECTORY/start-web-app.service /etc/systemd/system` to copy the service files from the git directory to        the /etc/systemd/system directory so that they start their respective Python files on somputer boot up.
   
7. Run `systemctl daemon-reload` to tell the computer that there are new service files to be run at startup.

8. Run `systemctl enable --now send-node-metrics.service` and `systemctl enable --now start-web-app.service.` to enable the      services.

9. Run `nano metrics.py` to edit 'metrics.py' (if nano isn't installed, install it by running `apt-get install nano`)

10. In 'metrics.py' in the getDiskInfo() function, there is a command that should be, or look similar to: 
   `getDevices = str(subprocess.check_output('~/waggleWebAPI/detectDiskDevices.sh', shell=True).decode('ascii'))`
   Change the path in the parentheses of the `subprocess.check_output()` to the path of the `detectDiskDevices.sh` where the    git repo was cloned (should still be the current directory you are in). Save the file and exit nano by typing ctrl-o, then    ctrl-x.
   
11. Run `nano send-node-metrics.service` and change the line that looks like: 
    `ExecStart=/usr/bin/python2.7 /root/waggleWebAPI/sendData.py` so that the path to 'sendData.py' is correct. Save and         exit.

12. Repeat step 11 for `start-web-app.service` so that the path to 'waggleApp.py' is correct. Save and exit.

13. Run `nano sendData.py` and change the 'dir' variable at the beginning of the code to the path to the                         beehive-dev-node-0000-code directory.

14. Restart the computer and everything should be working!


**Future Installation Improvements:** Ideally, the install.sh script would work, and only that file would need to be run in order to install this API. However, the install script wasn't able to be finished before the end of the summer, so the steps above are the way to install everything for right now. In addition, it would be ideal if the install.sh script would be able to set locales without the graphical user interface and ask the user for directory locations for the services, sendData.py, and metrics.py files so that the directory locations do not have to be changed manually.
