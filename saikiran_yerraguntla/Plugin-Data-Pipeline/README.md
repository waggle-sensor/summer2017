# What is the Plugin-Data-Pipeline (a.k.a PDP)

In order to test certain software via virtual nodes and observe how the data is parsed through the server and outputted to a web-interface, various plugins clients must be set up to process such data formulated by the software.
Thus, this documentation instructs you on how you can create and run your own your node-side and server-side plugins. Using this documentation, tutorials provided below and the existing virtual nodes, you can create node-side plugins that will test your software, through a publisher script, and implement server-side plugins, through a worker-client script, that can process and handle the incoming i/o from the node-side plugin.

The following sections below will explain on how to install the corresponding packages and dependencies, and will provide the steps to make your own publisher and worker scripts for software-analysis through Waggle's Beehive server.


# Installation

  * [PyWaggle](https://github.com/waggle-sensor/pywaggle.git)
  * [OpenSSL/TLS Certification & Registeration]()
  * [Hello Publisher](https://github.com/seanshahkarami/hello-publisher.git)
                     

# Steps to setup PDP

  1.   `  cd $HOME`
  
  2.   `  mkdir plugin`
  
  3.   `  sudo apt-get update`
  
  4.   `  sudo apt-get upgrade`
  
  5.   `  sudo apt-get install git`
  
  6.   `  cd plugin`
  
  7.   `  git clone https://github.com/sai6kiran/Plugin-Data-Pipeline.git`
  
  8.   `  mkdir test`
  
  9.   `  cd test`
  
  10.   `  cp ~/plugin/Plugin-Data-Pipeline/requirements.txt ~/plugin/test`
  
  11.   `  apt-get install python3-pip`
  
  12.   `  pip3 install -U -r requirements.txt`
  
  13.   Retrieve vnodes certificates and keys, in the form a compressed folder, from mentor.
  
  14.   `  mv ~/Downloads/vnode.tar.gz ~/plugin`
  
  15.   `  tar xzf ~/plugin/vnode.tar.gz`
  
  16.   `  mv ~/plugin/Plugin-Data-Pipeline/cacert.pem ~/plugin`
  
  17.   Now Create and run your plugin script.
     


# How to use PDP

VNE mainly comprises of two scripts, you the developer, must implement. The publisher script (node-side plugin) and the worker script (server-side plugin). Below is a diagram illustrating a model of how the end-to-end communication takes place between a publisher and a consumer/database.

|    Creating the Publisher Script:    |    Creating the Worker Script:    |
|:---------------|:--------------|
|The following module will explain how to implement the outershell of your plugin client.|The following module will explain how to implement the outershell of your worker script.|
|`#!/usr/bin/env python3`|`#!/usr/bin/env python3`|                
|`from waggle import beehive`| `from waggle import beehive` |
|`import pika`| `import pika` |
|The following packages and dependicies to import in order to run plugin. Other packages can be imported.|The following packages and dependicies to import in order to run worker client. Other packages can be imported.|
|`n="(n)"`|`n="(n)"` |
|Specifiy the number of which virtual node you wish to send your plugin data to. The data will then be sent to virtual node: 000002000000000(n-1).|Specifiy the number of which virtual node you wish to send your plugin data to. The data will then be sent to virtual node: 000002000000000(n-1).|
|`config = beehive.ClientConfig(`|`config = beehive.ClientConfig(`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`host='beehive.mcs.anl.gov',`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`host='beehive.mcs.anl.gov',`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`port=23181,`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`port=23181,`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`node='000002000000000'+str(int(n)-1),`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`node='000002000000000'+str(int(n)-1),`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`username = '(username1)',`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`username = '(username2)',`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`password = '(password1)'`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`password = '(password2)'`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cacert='~/plugin/cacert.pem',`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cacert='~/plugin/cacert.pem',`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cert='~/plugin/vnode/vnode'+str(int(n))+'/cert.pem',`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cert='~/plugin/vnode/vnode'+str(int(n))+'/cert.pem',`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`key='~/plugin/vnode/vnode'+str(int(n))+'/key.pem')`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`key='~/plugin/vnode/vnode'+str(int(n))+'/key.pem')`|
|The Config function initalizes your config paramters, allowing you to: Connect to beehive-dev's rabbitmq server, Connect and transmit data to the virtual node, and use certificates for authentiction purposes.|The Config function initalizes your config paramters, allowing you to: Connect to beehive-dev's rabbitmq server, Connect and transmit data to the virtual node, and uses certificates for authentication purposes.|
| **Default username1=fib-publisher , password1=waggle** |  **Default username2=worker-fib , password=waggle** |
| | **Your code will be placed in this part of the script.** |
|`client = beehive.PluginClient(` | `def callback(data):`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`name=test:1,`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`value = data.get('body')`|
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`config=config)`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return(value)`|
|This Client function allows you to create your client script and connection. It allows you to declare a queue to send all your information and sets your configuration parameters.|Receiving messages from the queue is more complex. It works by subscribing a callback function to a queue. Whenever you receive a message, this callback function is called by the Pika library. In this case the function will send the ouput to beehive-dev's interface: [http://10.10.10.5/?all=true](http://10.10.10.5/?all=true)
| **Your code will be placed in this part of the script.** |
|At the end of your program, in order to send your data/plugin to rabbitmq server, you must add the following line of code:|`client = beehive.PluginClient(`|
|`client.publish('(key)', (value))`|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`name=test:1,`|
|Sends it with a key and value.|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`config=config,`|
| |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`callback=callback)`|
| | This Client function allows you to create your client script and connection. It allows you to declare a queue to send all your information and sets your configuration parameters & callback function.|

# Outcome of PDP

The data sent by your node-side plugin is sent to db-raw at: http://10.10.10.5/?all=true

The processed data, done by server-side plugin, is sent to db-decoded to: http://10.10.10.5/?all=true

The following output data is in the form of a file that can be downloaded from the website. This website is beehive-dev's web interface.


# Sample Use of PDP

The following section will display a sample node-side plugin script and server-side plugin script used to send and process data through communication with beehive-dev.

The following code demonstrates a simple fibonacci program that runs within beehive-dev and computes the fibonacci number of any data, in the form of a number, sent through the plugin.

| Publisher Script: | Worker Script: |
|:------------------|:-----------------|
|![image 1](https://user-images.githubusercontent.com/25256730/28250983-a740e8b6-6a39-11e7-88b3-9a71f368088d.png)|![image](https://user-images.githubusercontent.com/25256730/28250974-96f004c4-6a39-11e7-96d9-470f9cf822b7.png)|


# Further Implications

You can also test your node-side and server-side plugins through a virtual node. Check the repository below, to learn how to create your own virutal nodes and how to run your plugins virtually.

 * [Virtual-Node-Environment](https://github.com/sai6kiran/Virtual-Node-Environment.git)
