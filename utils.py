from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from skimage import color

import pyautogui
import time
import math

import numpy
import cv2


def numberOfColors(filename):
	img = Image.open(filename)
	img = numpy.array(img)

	n = len(img)
	m = len(img[0])

	s = set()

	for i in range(0, n):
		for j in range(0, m):
			x = img[i][j][0]
			x *= 255

			x += img[i][j][1]
			x *= 255

			x += img[i][j][2]

			s.add(x)

	print('Number of colors in %s: %d' % (filename, len(s)))


def swapRB(img):
	n = len(img)
	m = len(img[0])

	for i in range(0, n):
		for j in range(0, m):
			img[i][j][0], img[i][j][2] = img[i][j][2], img[i][j][0]


def isEqualPixel(pixel1, pixel2):
	for i in range(0, 3):
		if pixel1[i] != pixel2[i]:
			return False

	return True


def isSimilarColor(color1, color2, threshold):
	# Red Color
	r1 = color1[0]/256
	g1 = color1[1]/256
	b1 = color1[2]/256

	r2 = color2[0]/256
	g2 = color2[1]/256
	b2 = color2[2]/256

	color1_lab = color.rgb2lab([r1, g1, b1])
	color2_lab = color.rgb2lab([r2, g2, b2])

	# Find the color difference
	delta_e = 0

	for i in range(0, 3):
		delta_e += (color1_lab[i]-color2_lab[i])**2

	delta_e = math.sqrt(delta_e)

	return delta_e <= threshold


def binStrToChar(s):
	n = len(s)
	res = 0

	for i in range(n-1, -1, -1):
		res *= 2

		if s[i] == '1':
			res += 1

	return chr(res)


def charToBinStr(c):
	num = ord(c)
	res = ''
	i = 8

	while i > 0:
		res += chr((num%2)+ord('0'))
		num //= 2
		i -= 1

	return res


def binStrToInt(s):
	n = len(s)
	res = 0

	for i in range(n-1, -1, -1):
		res *= 2

		if s[i] == '1':
			res += 1

	return res


def intToBinStr(num, bytes):
	res = ''
	i = bytes*8

	while i > 0:
		res += chr((num%2)+ord('0'))
		num //= 2
		i -= 1

	return res


def strToBinStr(s):
	n = len(s)
	res = ''

	for i in range(0, n):
		res += charToBinStr(s[i])

	return res


def binStrToStr(s):
	n = len(s)
	res = ''

	for i in range(0, n, 8):
		res += binStrToChar(s[i:i+8])

	return res

def captureScreenshot(x1, y1, x2, y2, time_interval, destination_filename):
	im = pyautogui.screenshot()
	im = im.crop((x1, y1, x2, y2))
	im.save(destination_filename)
	time.sleep(time_interval)


def convertFormat(source_filename, destination_filename):
	img = Image.open(source_filename)
	img = numpy.array(img)
	swapRB(img)

	cv2.imwrite(destination_filename, img)


def reduceColorsUsingKmeans(source_filename, destination_filename, n_colours=32):
	img = Image.open(source_filename)
	img = numpy.array(img)

	img = numpy.array(img)

	w, h, d = original_shape = img.shape

	n = len(img)
	m = len(img[0])

	new_img = []

	for i in range(0, n):
		new_img.append([])

		for j in range(0, m):
			new_img[i].append(color.rgb2lab(img[i][j]))

	new_img = numpy.array(new_img)
	image_array = new_img.reshape(w*h,d)

	kmeans = KMeans(n_clusters=n_colours).fit(image_array)

	labels = kmeans.labels_

	def recreate_image(centroids, labels, w, h):
		d = centroids.shape[1]
		image = numpy.zeros((w, h, d))
		label_idx = 0

		for i in range(w):
			for j in range(h):
				new_pixel = color.lab2rgb(centroids[labels[label_idx]])

				image[i][j][0] = int(256*new_pixel[0])
				image[i][j][1] = int(256*new_pixel[1])
				image[i][j][2] = int(256*new_pixel[2])

				label_idx += 1

		return image

	new_img = recreate_image(kmeans.cluster_centers_, labels, w, h)

	new_img = new_img.tolist()
	swapRB(new_img)
	new_img = numpy.array(new_img)

	cv2.imwrite(destination_filename, new_img)


def drawOutline(source_filename, destination_filename, retain_color):
	img = numpy.array(Image.open(source_filename))

	n = len(img)
	m = len(img[0])

	new_img = []

	for i in range(0, len(img)):
		new_img.append([])

		for j in range(0, len(img[i])):
			new_img[i].append(numpy.array([0, 0, 0]))

	new_img = numpy.array(new_img)

	for i in range(0, len(img)):
		for j in range(0, len(img[i])):
			if i-1 < 0 or j-1 < 0 or i+1 == n or j+1 == m:
				if retain_color:
					new_img[i][j] = numpy.array(img[i][j])
				else:
					new_img[i][j] = numpy.array([255, 255, 255])

				continue

			flag = False

			if not isEqualPixel(img[i-1][j], img[i][j]):
				flag = True
			if not isEqualPixel(img[i+1][j], img[i][j]):
				flag = True
			if not isEqualPixel(img[i][j-1], img[i][j]):
				flag = True
			if not isEqualPixel(img[i][j+1], img[i][j]):
				flag = True
			if not isEqualPixel(img[i-1][j-1], img[i][j]):
				flag = True
			if not isEqualPixel(img[i-1][j+1], img[i][j]):
				flag = True
			if not isEqualPixel(img[i+1][j-1], img[i][j]):
				flag = True
			if not isEqualPixel(img[i+1][j+1], img[i][j]):
				flag = True
				
			if flag:
				if retain_color:
					new_img[i][j] = numpy.array(img[i][j])
				else:
					new_img[i][j] = numpy.array([255, 255, 255])

	if retain_color:
		swapRB(new_img)

	cv2.imwrite(destination_filename, new_img)


def drawIntelligentOutline(source_filename, destination_filename, retain_color, threshold):
	img = numpy.array(Image.open(source_filename))

	n = len(img)
	m = len(img[0])

	new_img = []

	for i in range(0, len(img)):
		new_img.append([])

		for j in range(0, len(img[i])):
			new_img[i].append(numpy.array([0, 0, 0]))

	new_img = numpy.array(new_img)

	for i in range(0, len(img)):
		for j in range(0, len(img[i])):
			if i-1 < 0 or j-1 < 0 or i+1 == n or j+1 == m:
				if retain_color:
					new_img[i][j] = numpy.array(img[i][j])
				else:
					new_img[i][j] = numpy.array([255, 255, 255])

				continue

			flag = False

			if not isSimilarColor(img[i-1][j], img[i][j], threshold):
				flag = True
			if not isSimilarColor(img[i+1][j], img[i][j], threshold):
				flag = True
			if not isSimilarColor(img[i][j-1], img[i][j], threshold):
				flag = True
			if not isSimilarColor(img[i][j+1], img[i][j], threshold):
				flag = True
			if not isSimilarColor(img[i-1][j-1], img[i][j], threshold):
				flag = True
			if not isSimilarColor(img[i-1][j+1], img[i][j], threshold):
				flag = True
			if not isSimilarColor(img[i+1][j-1], img[i][j], threshold):
				flag = True
			if not isSimilarColor(img[i+1][j+1], img[i][j], threshold):
				flag = True
				
			if flag:
				if retain_color:
					new_img[i][j] = numpy.array(img[i][j])
				else:
					new_img[i][j] = numpy.array([255, 255, 255])

	if retain_color:
		swapRB(new_img)

	cv2.imwrite(destination_filename, new_img)

