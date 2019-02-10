import cv2
import numpy as np

class yolov3(object):
	def __init__(self, dimension, config = "dat/yolov3.cfg.txt",classes="dat/yolov3.txt", weights="dat/yolov3.weights"):
		with open(classes, 'r') as f:
		    self.classes = [line.strip() for line in f.readlines()]
		self.net = cv2.dnn.readNet(weights, config)
		self.COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
		self.dimension = dimension[1], dimension[0]


	def get_output_layers(self):
	    layer_names = self.net.getLayerNames()
	    output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
	    return output_layers


	def draw_prediction(self, image, class_id, confidence, x, y, x_plus_w, y_plus_h):
	    label = str(self.classes[class_id])
	    color = tuple(map(int,self.COLORS[class_id]))
	    x, y, x_plus_w, y_plus_h = tuple(map(int,[x, y, x_plus_w, y_plus_h]))
	    image = np.array(image)
	    cv2.rectangle(image, (x, y), (x_plus_w, y_plus_h), color, 1)
	    cv2.putText(image, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
	    return np.array(image)

	def preprocess(self, image, scale=0.00392):
		Width = image.shape[1]
		Height = image.shape[0]
		blob = cv2.dnn.blobFromImage(image, scale, self.dimension, (0,0,0), True, crop=False)
		self.net.setInput(blob)
		return Width, Height

	def feedforward(self, Width, Height):
		outs = self.net.forward(self.get_output_layers())
		class_ids, confidences, boxes = [], [], []
		for out in outs:
		    for detection in out:
		        scores = detection[5:]
		        class_id = np.argmax(scores)
		        confidence = scores[class_id]
		        if confidence > 0.5:
		            center_x = int(detection[0] * Width)
		            center_y = int(detection[1] * Height)
		            w = int(detection[2] * Width)
		            h = int(detection[3] * Height)
		            x = center_x - w / 2
		            y = center_y - h / 2
		            class_ids.append(class_id)
		            confidences.append(float(confidence))
		            boxes.append([x, y, w, h])
		return class_ids, confidences, boxes

	def postprocess(self, image, class_ids, confidences, boxes, conf_threshold = 0.1, nms_threshold = 0.4):  #conf = 05, nms = 0.4
		indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
		cv2.rectangle(image, (0, 0), (300, 300), self.COLORS[2], 20)
		for i in indices:
		    i = i[0]
		    box = boxes[i]
		    x = box[0]
		    y = box[1]
		    w = box[2]
		    h = box[3]
		    image = self.draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
		cv2.imshow("object detection", image)
		return image

	def forward_pass(self, image):
		Width, Height = self.preprocess(image)
		class_ids, confidences, boxes = self.feedforward(Width, Height)
		return self.postprocess(image, class_ids, confidences, boxes)	










