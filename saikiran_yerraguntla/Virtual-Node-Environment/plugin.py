#!/usr/bin/env python3
from waggle import beehive
import pika
import waggle.pipeline
import time
import sys
import os
import subprocess
import json
from coresense import create_connection, NoPacketError



#Upgrade PyWaggle module
os.system('pip3 install git+https://github.com/waggle-sensor/pywaggle')

#Start RabbitMQ Server
os.system('rabbitmq-server start &')
time.sleep(25)
################################################################################

output = os.popen('curl --unix-socket /var/run/docker.sock http:/containers/json').read()
#print(output)

python_dict = json.loads(output)

containers=[]
for dict in python_dict:
        containers.append(dict['Id'])
        #print(dict['Id'])


waggle_output = os.popen('find /dev -name "waggle_coresense[0-9]*"').readlines()
waggle_output = list(map(lambda s: s.strip(), waggle_output))
print(waggle_output)

print(containers)
containers.sort()
print(containers)

bind_dict = {}
for i in range(len(waggle_output)):      #Since (Number of Containers) >= (Number of Waggle Coresense Boards).
        bind_dict[containers[i]] = waggle_output[i]

print(bind_dict)

node_dict = {}
node_output = os.popen('find /usr/lib/waggle/SSL/vnode/ -mindepth 1 -name "vnode*"')
node_output = list(map(lambda t: t.strip(), node_output))
for i in range(len(waggle_output)):
    node_dict[containers[i]] = node_output[i]

print(node_dict)

command = "cat /proc/self/cgroup | grep 'docker' | sed 's/^.*\///' | tail -n1"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
container_id = process.communicate()
container_id = container_id[0].decode("utf-8").rstrip()
print(container_id)

#if container_id in bind_dict:
    #print(bind_dict[container_id])

src = bind_dict[container_id]
dest = '/dev/waggle_coresense'
os.symlink(src, dest)

config = beehive.ClientConfig(
    host='10.10.10.5',
    port=23181,
    node='000002000000000'+ str(int((node_dict[container_id])[-1])-1),
    username = 'fib-publisher',
    password = 'waggle',
    cacert='/usr/lib/waggle/SSL/waggleca/cacert.pem',
    cert= node_dict[container_id]+'/cert.pem',
    key= node_dict[container_id]+'/key.pem')


client = beehive.PluginClient(
    name='test:1',
    config=config)


device = os.environ.get('CORESENSE_DEVICE', '/dev/waggle_coresense')

while True:
    try:
        print('Connecting to device: {}'.format(device), flush=True)

        with create_connection(device) as conn:
            print('Connected to device: {}'.format(device), flush=True)

            while True:
                message = conn.recv()
                if message is not None:
                    print('Received frame.', flush=True)
                    #self.send(sensor='frame', data=message.frame)
                    client.publish('frame', message.frame)
                time.sleep(5)
    except NoPacketError:
        print('No packets are being received. Resetting the serial connection...')
