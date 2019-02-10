import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'resources/sad.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.face_detection(image=image)
labels = response.face_annotations

print('Joy Score: {}'.format(label.joy_likelihood))
print('Anger Score: {}'.format(label.anger_likelihood))
print('Sorrow Score: {}'.format(label.sorrow_likelihood))
print('blurred Score: {}'.format(label.blurred_likelihood))
print('Surprise Score: {}'.format(label.surprise_likelihood))