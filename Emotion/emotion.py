import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 


# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client

def getEmotions(image):
	client_vision = vision.ImageAnnotatorClient()
	#print client_vision

	# The name of the image file to annotate
	image = types.Image(content=image)

	# Performs label detection on the image file
	response = client_vision.face_detection(image=image)
	label = response.face_annotations[0]

	#for label in labels:

	print('Joy Score: {}'.format(label.joy_likelihood))
	print('Anger Score: {}'.format(label.anger_likelihood))
	print('Sorrow Score: {}'.format(label.sorrow_likelihood))
	print('Surprise Score: {}'.format(label.surprise_likelihood))
