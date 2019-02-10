import paho.mqtt.client as mqtt
import ssl
import cv2
import numpy as np
from yolov3 import *

yolo = yolov3((480, 640))

def onConnect(client, userdata, flags, rc):
	print('connected!')
	client.subscribe('gameplay')

def onDisconnect(client, userdata, rc):
	print('disconnected!')

def onMessage(client, userdata, message):
	decoded = cv2.imdecode(np.frombuffer(message.payload, np.uint8), -1)
	yolo.forward_pass(decoded)

client = mqtt.Client(transport="websockets")
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.on_connect = onConnect
client.on_disconnect = onDisconnect
client.on_message = onMessage

client.username_pw_set('solace-cloud-client', password='1l9962hd8jum3sc6uvk34md96l')
client.connect('mr4b11zrabb.messaging.mymaas.net', 8443, 20)
client.loop_forever()