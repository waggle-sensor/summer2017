#!/usr/bin/env python3
from waggle import beehive
import pika
import os.path
import re
import json
import base64
import binascii
#from urllib.parse import urlencode

#url = 'amqp://sai6kiran:Cvv0ek@sky@10.10.10.5:10000'

#connection = pika.BlockingConnection(pika.URLParameters(host=url))
#channel = connection.channel

#channel.exchange_declare(exchange='test_exchange',
 #                        exchange_type='direct')

#channel.exchange_bind(source='data-pipeline-in',
 #                     destination='test_exchange')

#channel.queue_declare(queue='test_queue',
 #                     durable=True,
  #                    exclusive=True)

#channel.queue_bind(queue='test_queue',
 #                  exchange='test_exchange',
 #                  routing_key='test')

#channel.exchange_declare(exchange='plugins_out',
 #                        exchange_type='fanout',
                    #How to only send to db-decoded queue, as this exchange is fanout to plenario as well.
#                         durable=True)

config = beehive.ClientConfig(
    host = '10.10.10.5',
    port = 23181,
    username = 'fib-worker',
    password = 'waggle',
    cacert = '/home/sai6kiran/worker/cacert.pem',
    cert = '/home/sai6kiran/worker/cert.pem',
    key = '/home/sai6kiran/worker/key.pem')

#Fibonacci Function
def fib(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)

def callback(data):
   # num = body.decode()
    #int_num = int(str(num))
    #regex = r"([a-zA-Z]+) (\d+)"
    #match = re.search(regex, num)
    #n = float(match.group(1))
    stuff = data.get('body')
    data = base64.b64decode(stuff)
    fib_val = fib(int(str(data, 'utf-8')))
    print(fib_val)
    #print(base64.b64decode(stuff))
    #print(base64.b64decode(str.encode(stuff)))
    #print(type(data))
    #print(int(str(data, 'utf-8')))
    #fib_value = fib(int(data.get('body'),16))
    #print("here number:" , fib_value)
    return(str(fib_val))
    #channel.basic_publish(properties=properties,
      #                    exchange='plugins-out',
     #                     routing_key=method.routing_key,
    #                      body=data)

   # ch.basic_ack(delivery_tag=method.delivery_tag)

client = beehive.WorkerClient(
    name = 'test:1',
    config=config,
    callback = callback)

client.start_working()
