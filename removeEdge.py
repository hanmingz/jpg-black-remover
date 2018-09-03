import numpy as np 
import cv2
import os
from os import listdir
from os.path import isfile, join
import glob

edgeW = 60
edgeH = 60

middle_cascade = cv2.CascadeClassifier('cascade.xml')

dname = os.getcwd()

i = 0
for f in glob.glob('input/*.jpg'):

	img = cv2.imread(f, 0)
	width, height = img.shape[:2]
	text = img[edgeW: width-edgeW, edgeH:height-edgeH]
	width, height = text.shape[:2]
	dark = middle_cascade.detectMultiScale(text, 1.15, 5)

	ctr = []
	top = height
	bottom = 0
	for (x,y,w,h) in dark:
		if y > height / 2 - 100 and y < height / 2 + 300:
			ctr.append(y)
			if y < top:
				top = y

			if y + h > bottom:
				bottom = y + h

	ctr.sort()
	length = len(ctr) 
	if length > 3:
		ctr.pop(0)
		ctr.pop(length - 2)

	if len(ctr) != 0:
		ave = int(sum(ctr) / len(ctr))
		cv2.rectangle(text, (0, ave - 30), (width, ave + 100), 255, -1)

	cv2.imwrite(f'{os.path.splitext(f)[0]}.jpg', text)
	i = i + 1
