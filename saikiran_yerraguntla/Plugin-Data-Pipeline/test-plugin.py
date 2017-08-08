#!/usr/bin/env python3
from waggle import beehive
import pika
import time
import sys
import base64

config = beehive.ClientConfig(
    host='10.10.10.5',
    port=23181,
    node='0000020000000005',
    username = 'fib-publisher',
    password = 'waggle',
    cacert='/home/sai6kiran/worker/cacert.pem',
    cert='/home/sai6kiran/worker/cert.pem',
    key='/home/sai6kiran/worker/key.pem')

client = beehive.PluginClient(
    name='test:1',
    config=config)

#class FibonacciRpcPlugin(object):
 #   def __init__(self):
  #      def on_response(self, ch, method, props, body):
   #         self.response = body
    #def call(self, n):
     #   client.publish(response,str(n))

      #  while self.response is None:
       #     self.connection.process_data_events()
        #return int(self.response)


#fibonacci_rpc = FibonacciRpcPlugin()

#response = fibonacci_rpc.call(20)
while True:
    try:
        num = 12
        data_string = '%s' % (num)
        bytes1 = str.encode(data_string)
        print(bytes1)
        client.publish("fib_value", data_string)###base64.b64encode(bytes1))
        time.sleep(1)
    except KeyboardInterrupt:
        break
