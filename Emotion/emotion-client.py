import paho.mqtt.client as mqtt
import ssl
import cv2
import numpy as np
from emotion import *

def onConnect(client, userdata, flags, rc):
	print('connected!')
	client.subscribe('video')

def onDisconnect(client, userdata, rc):
	print('disconnected!')

def onMessage(client, userdata, message):
	decoded = cv2.imdecode(np.frombuffer(message.payload, np.uint8), -1)
	#joy, sorrow, anger, surprise = getEmotions(message.payload)
	getEmotions(message.payload)
	# cv2.putText(decoded, "Joy: " + str(joy), (425,300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 0, 0), 1)
	# cv2.putText(decoded, "Sorrow: " + str(sorrow), (425,275), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 225, 0), 1)
	# cv2.putText(decoded, "Anger: " + str(anger), (425,250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 225), 1)
	# cv2.putText(decoded, "Surprise" + str(surprise), (425,225), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (125, 125, 0), 1)
	cv2.imshow("Emotion", decoded)
	cv2.waitKey(1)


client = mqtt.Client(transport="websockets")
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.on_connect = onConnect
client.on_disconnect = onDisconnect
client.on_message = onMessage

client.username_pw_set('solace-cloud-client', password='1l9962hd8jum3sc6uvk34md96l')
client.connect('mr4b11zrabb.messaging.mymaas.net', 8443, 20)
client.loop_forever()