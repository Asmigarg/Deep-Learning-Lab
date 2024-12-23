# -*- coding: utf-8 -*-
"""Experiment 5(YOLO).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1S0FPBgxyok4qMCDROawkw5zcw3vGxz9D
"""

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

print("LOADING YOLO")
net=cv2.dnn.readNet("yolov3.weights","yolov3.cfg")

classes = []
with open("coco.names", "r") as f:
  classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()

output_layers = [layer_names[i - 1] for i in
net.getUnconnectedOutLayers()]
print("YOLO LOADED")

img = cv2.imread("person.jpg")
img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape
print("Input Image:")
cv2_imshow(img)

blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True,crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

class_ids = []
confidences = []
boxes = []
for out in outs:
  for detection in out:
    scores = detection[5:]
    class_id = np.argmax(scores)
    confidence = scores[class_id]
    if confidence > 0.3:
      center_x = int(detection[0] * width)
      center_y = int(detection[1] * height)
      w = int(detection[2] * width)
      h = int(detection[3] * height)
      x = int(center_x - w / 2)
      y = int(center_y - h / 2)
      boxes.append([x, y, w, h])
      confidences.append(float(confidence))
      class_ids.append(class_id)

# We use NMS function in opencv to perform Non-maximum Suppression
# we give it score threshold and nms threshold as arguments.
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

colors = np.random.uniform(0, 255, size=(len(classes), 3))
for i in range(len(boxes)):
  if i in indexes:
    x, y, w, h = boxes[i]
    label = str(classes[class_ids[i]])
    color = colors[class_ids[i]]

# Draw the bounding box
cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
# Draw the label
cv2.putText(img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1/2, color, 2)
print(f"Detected object: {label}, confidence: {confidences[i]}, box: {x}, {y}, {w}, {h}")

# Display the image
cv2_imshow(img)
cv2.waitKey(0)

