from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import numpy
import cv2


def equalPixels(rgb1, rgb2):
	r1 = rgb1[0]
	b1 = rgb1[1]
	g1 = rgb1[2]

	r2 = rgb2[0]
	b2 = rgb2[1]
	g2 = rgb2[2]

	return (r1 == r2 and b1 == b2 and g1 == g2)


def generateIntermediate(source_filename, destination_filename, n_colours):
	img = Image.open(source_filename)
	img = numpy.array(img)

	img = numpy.array(img)

	w, h, d = original_shape = img.shape
	image_array = img.reshape(w*h,d)

	kmeans = KMeans(n_clusters=n_colours).fit(image_array)

	labels = kmeans.labels_

	def recreate_image(centroids, labels, w, h):
		d = centroids.shape[1]
		image = numpy.zeros((w, h, d))
		label_idx = 0

		for i in range(w):
		    for j in range(h):
		        image[i][j] = centroids[labels[label_idx]]
		        label_idx += 1

		return image

	temp_ci = recreate_image(kmeans.cluster_centers_, labels, w, h)
	temp_ci = temp_ci.tolist()

	for i in range(0, len(temp_ci)):
		for j in range(0, len(temp_ci[i])):
			for k in range(0, len(temp_ci[i][j])):
				temp_ci[i][j][k] = int(temp_ci[i][j][k])
				temp_ci[i][j][k] = max(0, temp_ci[i][j][k])
				temp_ci[i][j][k] = min(255, temp_ci[i][j][k])

			ttc = []
			ttc.append(temp_ci[i][j][2])
			ttc.append(temp_ci[i][j][1])
			ttc.append(temp_ci[i][j][0])

			temp_ci[i][j] = ttc

	img = numpy.array(temp_ci)

	n = len(img)
	m = len(img[0])

	new_img = img.copy()

	for i in range(0, len(img)):
		for j in range(0, len(img[i])):
			if i-1 < 0 or j-1 < 0 or i+1 == n or j+1 == m:
				continue

			flag = True

			if not equalPixels(img[i-1][j], img[i][j]):
				flag = False
			if not equalPixels(img[i+1][j], img[i][j]):
				flag = False
			if not equalPixels(img[i][j-1], img[i][j]):
				flag = False
			if not equalPixels(img[i][j+1], img[i][j]):
				flag = False
			if not equalPixels(img[i-1][j-1], img[i][j]):
				flag = False
			if not equalPixels(img[i-1][j+1], img[i][j]):
				flag = False
			if not equalPixels(img[i+1][j-1], img[i][j]):
				flag = False
			if not equalPixels(img[i+1][j+1], img[i][j]):
				flag = False
				
			if flag:
				new_img[i][j] = numpy.array([0, 0, 0])

	cv2.imwrite(destination_filename, new_img)

