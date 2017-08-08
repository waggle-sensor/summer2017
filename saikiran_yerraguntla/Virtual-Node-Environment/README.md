# What is VNE

The Virtual Node Environment (VNE) is a tool created to implement and deploy virtual nodes that would run various processes and software plugins. The creation and production of numerous hardware nodes can be expensive, time-consuming and tough to scale. However, vital objectives such as plugin development, automated software testing, stress-testing the server are inhibited
without using existing hardware pieces of the node. Thus, replicas of these nodes are created virtually for testing and experimental purposes.

The virtual machine that mirrors the exact functioning of a hard-node is the virtual node, and the environment that allows the creation, testing, and deployment of these virtual nodes, to an infinite number, is the Virtual Node Environment.
The applications used to allow the creation and deployment of these virtual nodes is Docker. Docker was used to create the virtual node and its environment as containers. The container would later be used for virtually running software plugins, creating a swarm of a multitude of nodes to stress-test the Waggle server for further development, laying a basis for further creation of more virtual nodes, and automate software testing.

Using this documentation, you will be able to create your own virtual node(s)!!!!! 


# Installation Requirements
  
  * [Install Docker](https://docs.docker.com/engine/installation/#supported-platforms) 
  * [Create an online Docker hub acocunt](https://hub.docker.com/)
  * Clone this repository: `git clone https://github.com/sai6kiran/Virtual-Node-Environment.git`
  * Clone the waggle image repository: `git clone https://github.com/sai6kiran/waggle_image.git`
 
  ### Optional
  
   * Clone the PyWaggle repository: `git clone https://github.com/waggle-sensor/pywaggle.git`
   * Clone the Plugin-Data-Pipeline repository: `git clone https://github.com/sai6kiran/Plugin-Data-Pipeline.git`
   

# Building the Docker Image

After clone this directory in your home directory, follow the specifed command below:

`cd $HOME`

This will direct you to your home directory.

`cd Virtual-Node-Environment`

This will bring you insde the VNE repoistory you cloned on your local machine.

`docker build -t waggle-vne-image:2.6.0-pre1 -f dockerfiles/waggle-vne-image .`

Execute this following docker build command to build your image from the waggle-vne-image dockerfile.

`docker images`

Runnning this command will provide you the list of docker images on your local machine.



# Creaing the Docker Container
The following section will describe a sample example of how to create your container(s) to run the coresense plugin virtually, when a coresense board is conected to you local machine.

The following information presented below is an instance of how to use this tool in a certain way. This tool can be used to preform other actions, a node would preform, virtually.

There are two types of ways to create your own virtual node container(s):

### 1. Running it as a Unit-Container:

This section will explain how you can intialize your image to run as a single container. You can enter into your own virtual node container and explore & experiment with it however required.

 * Install the virtual node certificates to your local machine. Copy and save the folder, containing all the cert.pem and        key.pem files of each virual node, in your: `/etc/ssl` directory of your local machine.
 
 * Create a directory in your: `/etc/ssl` directory, named **_waggleca_**. Move the waggle cacert.pem, from the Virtual-Node-Environment directory to the foldeer WaggleCa
 
    `mv ~/Virtual-Node-Environment/cacert.pem /etc/ssl/waggleca` 
 
 * The command below will create a directory in udev directory of your local machine:
    
    `cd /etc/udev`
    
    `mkdir rules.d`
 
 * Now, move the udev rules script in the Virtual-Node-Environment directory to rules.d
     
     `mv 75-waggle-arduino.rules /etc/udev/rules.d`
 
 * Run the udev rules script. This will create symlinks in your `/dev` directory whenever a coresense, metasense or gps board is connected to your local machine.
     
     `udevadm control --reload`
 
 * Connect the coresense baord(s) to your machine.
 
***Run the following command to initialize your single container:***

    `docker run -it -v /etc/ssl/:/usr/lib/waggle/SSL -v /var/run/docker.sock:/var/run/docker.sock -v ~/Virtual-Node-Environment/plugin.py:/usr/lib/waggle/plugin_manager/plugins/coresense_3/plugin.py -t -i --device=/dev/waggle_coresense0:/dev/waggle_coresense0 -t -i --device=/dev/waggle_coresense1:/dev/waggle_coresense1 --workdir /usr/lib/waggle/plugin_manager/plugins/coresense_3 sai6kiran/waggle-vne-image:2.6.0-pre1`
     
 This will direct you inside the container, and now you can run your sotfware through a node virtually.
 
  ***To have the container to run the coresense_plugin in the background, specify the following run command:***
 
    `docker run -it -v /etc/ssl/:/usr/lib/waggle/SSL -v /var/run/docker.sock:/var/run/docker.sock -v ~/Virtual-Node-Environment/plugin.py:/usr/lib/waggle/plugin_manager/plugins/coresense_3/plugin.py -t -i --device=/dev/waggle_coresense0:/dev/waggle_coresense0 -t -i --device=/dev/waggle_coresense1:/dev/waggle_coresense1 --workdir /usr/lib/waggle/plugin_manager/plugins/coresense_3 sai6kiran/waggle-vne-image:2.6.0-pre1 ./plugin.py "hello world"`
    
This will run your coresense plugin, inside your container, in the background of your computer.
 
 ### 2. Running it as a swarm of containers:
 
This section will explain how you can intialize your image to run multiple containers simultaneously. 

 * Install the virtual node certificates to your local machine. Copy and save the folder, containing all the cert.pem and        key.pem files of each virual node, in your: `/etc/ssl` directory of your local machine.
 
 * Create a directory in your: `/etc/ssl` directory, named **_waggleca_**. Move the waggle cacert.pem, from the Virtual-Node-Environment directory to the foldeer WaggleCa
 
    `mv ~/Virtual-Node-Environment/cacert.pem /etc/ssl/waggleca` 
 
 * The command below will create a directory in udev directory of your local machine:
    
    `cd /etc/udev`
    
    `mkdir rules.d`
 
 * Now, move the udev rules script in the Virtual-Node-Environment directory to rules.d
     
     `mv 75-waggle-arduino.rules /etc/udev/rules.d`
 
 * Run the udev rules script. This will create symlinks in your `/dev` directory whenever a coresense, metasense or gps board is connected to your local machine.
     
     `udevadm control --reload`
 
 * Connect the coresense baord(s) to your machine.
 
 * Login to your docker account through your command line:
    
    `docker login`
 
 * Tag/rename your build image to match docker hub credentials.
    
    i.e. `docker tag waggle-vne-image:2.6.0-pre1 (__Your-username__)/waggle-vne-image:2.6.0-pre1`
    
 * Push your image from your local host to your docker hub repo:
    
    `docker push (__Your-username__)/waggle-vne-image:2.6.0-pre1`
    
 * Pull the image from your repo back to your local machine:
    
    `docker pull sai6kiran/waggle-vne-image:2.6.0-pre1`
 
 
  ***Run the following command to create your swarm of virtual nodes:***
 
    `docker service create --replicas (n) --name waggle-service --with-registry-auth --mount type=bind,src="/etc/ssl",dst="/usr/lib/waggle/SSL/" --mount type=bind,src="~/Virtual-Node-Environment/plugin.py",dst="/usr/lib/waggle/plugin_manager/plugins/coresense_3/plugin.py" --mount type=bind,src="/dev/waggle_coresense0",dst="/dev/waggle_coresense0" --mount type=bind,src="/dev/waggle_coresense1",dst="/dev/waggle_coresense1" --mount type=bind,src="/var/run/docker.sock",dst="/var/run/docker.sock" --workdir /usr/lib/waggle/plugin_manager/plugins/coresense_3/ sai6kiran/waggle-vne-image:2.6.0-pre1 ./plugin.py "hello world"`
 
  * Replace "(n)" with a number for the number of containers you wish deploy at once.
 
***Run the following command immediately after running your service of swarms:***

  `cd ~/Virtual-Node-Environment`

  `./container_listener.sh`

This will run a bash script that will listen for any active containers once the swarm is up. It will then send all required configuration information to the containers for all the coresense devices to be mounted on each and every container.


### 3. Debbuging:

The commands below are some debugging tools that can be used to fix any errors that may arise when running your docker containers.

  * Show a list of containers:
  
      `docker ps -a`
  
  * Stop all active containers:
  
      `docker stop $(docker ps -a -q)`
  
  * Remove all active containers:
  
      `docker rm $(docker ps -a -q)`
      
  * Show a list of services:
  
      `docker service ls`
      
  * Inspect a service running a swarm of containers:
      
      `docker service inspect <service-id>`
      
  * Remove a particular service:
      
      `docker service remove <service-id>`
   
  * Inspect the status of each task distributed to each worker/sub-container in the docker swarm:
      
      `docker service ps --no-trunc <service-name>`
      

# Tutorials

  * [Docker Tutorials](https://docs.docker.com/get-started/)
  * [Docker User-Guide](https://docs.docker.com/engine/userguide/)
  * [Docker Unit-Container cheat-sheet](https://docs.docker.com/engine/reference/commandline/run/)
  * [Docker swarm cheat-sheet](https://docs.docker.com/engine/reference/commandline/service_create/)
