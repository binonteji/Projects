import cv2
import numpy as np
import tensorflow as tf
import math

model = tf.keras.models.load_model('mdl.h5')

def padding_resizing(gray_img):
	org_size = 20
	img_size = 28
	ver, hor = gray_img.shape
	
	if ver > hor:
		factor = org_size/ver
		ver = org_size
		hor = int(round(hor*factor))        
	else:
		factor = org_size/hor
		hor = org_size
		ver = int(round(ver*factor))

	gray_img = cv2.resize(gray_img, (hor, ver))

	verPadding = (int(math.ceil((img_size-ver)/2.0)),int(math.floor((img_size-ver)/2.0)))
	horPadding = (int(math.ceil((img_size-hor)/2.0)),int(math.floor((img_size-hor)/2.0)))
	
	gray_img = np.lib.pad(gray_img,(verPadding,horPadding),'constant')

	return gray_img

def check(num):
	m = []
	for n in range(1, num + 1):
		img = cv2.imread('roi/{}.png'.format(n), 1)
		gray_img = (255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)) / 255
		th = padding_resizing(gray_img)
		flat_arr = th.reshape(-1,28,28,1)
		m.append(np.argmax(model.predict(flat_arr)))
	return m