import cv2
import predictor
from __main__ import *

def contoursFind():

	if(os.path.isfile('out.png') == False):
		pass
	else:
		img = cv2.imread('out.png', 1)
		image = (255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)) / 255
		
		# Scale and convert data type
		image_8bit = np.uint8(image * 255)

		#threshold_level = 127 
		_, binarized = cv2.threshold(image_8bit, 127, 255, cv2.THRESH_BINARY)
		contour_, _ = cv2.findContours(binarized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		r = []
		for cnt in contour_:
			x, y, w, h = cv2.boundingRect(cnt)
			r.append({'x' : x, 'y' : y, 'w' : w, 'h' : h}) 
			
		r = sorted(r, key=lambda e:[(e['x'])])
		a = 0
		for n in range(0,len(contour_)):
			yy = r[n].get('y')
			xx = r[n].get('x')
			ww = r[n].get('w')
			hh = r[n].get('h')
			cv2.rectangle(img, (xx, yy), (xx+ww, yy+hh), (0, 255, 0), 3)
			roi = img[yy:yy+hh, xx:xx+ww]
			a = a + 1
			cv2.imwrite('roi/{}.png'.format(a), roi)

	return predictor.check(len(contour_))
