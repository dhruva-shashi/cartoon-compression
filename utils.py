from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import pyautogui
import time

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


def convertToGreyScale(p):
	return (0.30*p[0])+(0.59*p[1])+(0.11*p[2])


def almostEqualPixels(p1, p2, diff):
	d = 0

	for i in range(0, 3):
		d += (p1[i]-p2[i])**2

	if d > diff:
		return False

	return True


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


def convertFormat(original_filename, destination_filename):
	img = Image.open(original_filename)
	img = numpy.array(img)

	n = len(img)
	m = len(img[0])

	for i in range(0, n):
		for j in range(0, m):
			img[i][j][0], img[i][j][2] = img[i][j][2], img[i][j][0]

	cv2.imwrite(destination_filename, img)

