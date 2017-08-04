import json
import pika
import time
import requests
import datetime


from metrics import sendMetrics, getGeneralInfo

sampleRate = 1 #how often the node should be pinged for metrics (in seconds)
genInfo = getGeneralInfo()

###if genInfo['Architecture'] == 'arm':
dir = "/home/waggle/waggleWebAPI/beehive-dev-node-0000-code"
###else:
    ###dir = "/home/adammorr/waggleWebAPI/beehive-dev-node-0000-code"
    

credentials = pika.credentials.PlainCredentials('node', 'waggle')

ssl_options={'ca_certs' : dir + "/cacert.pem",
             'certfile' : dir + "/node/cert.pem",
             'keyfile'  : dir + "/node/key.pem"}
#print ('ssl_options = ', ssl_options)

params = pika.ConnectionParameters(
                host="10.10.10.5", 
                port=23181, 
                credentials=credentials, 
                ssl=True, 
                ssl_options=ssl_options,
                retry_delay=10,
                socket_timeout=10)
#print ('params = {}'.format(params))

connection = pika.BlockingConnection(params)
#print ('connection = {}'.format(connection))

channel = connection.channel()
#print ('channel = {}'.format(channel))

while 1:
    time.sleep(sampleRate)

    properties = pika.BasicProperties(
            headers = {
                'value' : 80, 
                'reply_to' : "0000020000000000"},
            timestamp=int(datetime.datetime.utcnow().timestamp() * 1000),
            reply_to="0000020000000000")
    #print ('properties = {}'.format(properties))
    
    jsonData = sendMetrics()
    print (str(jsonData))
    channel.basic_publish(exchange='node-metrics', 
                    routing_key='', 
                    body=str(jsonData), 
                    properties=properties)

