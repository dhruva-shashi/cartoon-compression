import cv2
import numpy as np
from utils import *


def con_encode(source_filename, original_filename, destination_filename):
	img = cv2.imread(source_filename)
	img2 = cv2.imread(original_filename)

	n = len(img)
	m = len(img[0])

	components = []
	colored_points = []

	f = []

	for i in range(0, n):
		f.append([])
		for j in range(0, m):
			f[i].append(True)

	for i in range(0, n):
		for j in range(0, m):
			if not f[i][j]:
				continue

			r = img[i][j][0]
			g = img[i][j][1]
			b = img[i][j][2]

			if r != 255 or g != 255 or b != 255:
				continue

			a = []

			a.append([i, j])
			f[i][j] = False

			bfs_str = ''

			while len(a) > 0:
				x = a[0][0]
				y = a[0][1]

				a.pop(0)

				if x-1 >= 0 and img[x-1][y][0] == 255 and img[x-1][y][1] == 255 and img[x-1][y][2] == 255 and f[x-1][y]:
					bfs_str += '1'
					a.append([x-1, y])
					f[x-1][y] = False
				else:
					bfs_str += '0'

				if x+1 < n and img[x+1][y][0] == 255 and img[x+1][y][1] == 255 and img[x+1][y][2] == 255 and f[x+1][y]:
					bfs_str += '1'
					a.append([x+1, y])
					f[x+1][y] = False
				else:
					bfs_str += '0'

				if y-1 >= 0 and img[x][y-1][0] == 255 and img[x][y-1][1] == 255 and img[x][y-1][2] == 255 and f[x][y-1]:
					bfs_str += '1'
					a.append([x, y-1])
					f[x][y-1] = False
				else:
					bfs_str += '0'

				if y+1 < m and img[x][y+1][0] == 255 and img[x][y+1][1] == 255 and img[x][y+1][2] == 255 and f[x][y+1]:
					bfs_str += '1'
					a.append([x, y+1])
					f[x][y+1] = False
				else:
					bfs_str += '0'

			components.append([i, j, bfs_str])

	for i in range(0, n):
		for j in range(0, m):
			f[i][j] = True

	for i in range(0, n):
		for j in range(0, m):
			if not f[i][j]:
				continue

			r = img[i][j][0]
			g = img[i][j][1]
			b = img[i][j][2]

			if r == 255 and g == 255 and b == 255:
				continue

			rsum = 0
			gsum = 0
			bsum = 0

			a = []

			a.append([i, j])
			f[i][j] = False
			pixel_count = 0

			while len(a) > 0:
				x = a[0][0]
				y = a[0][1]

				a.pop(0)

				rsum += img2[x][y][0]
				gsum += img2[x][y][1]
				bsum += img2[x][y][2]

				pixel_count += 1

				if x-1 >= 0 and img[x-1][y][0] == 0 and img[x-1][y][1] == 0 and img[x-1][y][2] == 0 and f[x-1][y]:
					a.append([x-1, y])
					f[x-1][y] = False
				if x+1 < n and img[x+1][y][0] == 0 and img[x+1][y][1] == 0 and img[x+1][y][2] == 0 and f[x+1][y]:
					a.append([x+1, y])
					f[x+1][y] = False
				if y-1 >= 0 and img[x][y-1][0] == 0 and img[x][y-1][1] == 0 and img[x][y-1][2] == 0 and f[x][y-1]:
					a.append([x, y-1])
					f[x][y-1] = False
				if y+1 < m and img[x][y+1][0] == 0 and img[x][y+1][1] == 0 and img[x][y+1][2] == 0 and f[x][y+1]:
					a.append([x, y+1])
					f[x][y+1] = False

			r = rsum//pixel_count
			g = gsum//pixel_count
			b = bsum//pixel_count

			colored_points.append([i, j, r, g, b])

	final_str = ''
	final_str += intToBinStr(n)
	final_str += intToBinStr(m)
	final_str += intToBinStr(len(components))

	for component in components:
		final_str += intToBinStr(component[0])
		final_str += intToBinStr(component[1])
		final_str += intToBinStr(len(component[2]))
		final_str += component[2]

	final_str += intToBinStr(len(colored_points))

	for point in colored_points:
		final_str += intToBinStr(point[0])
		final_str += intToBinStr(point[1])
		final_str += intToBinStr(point[2])
		final_str += intToBinStr(point[3])
		final_str += intToBinStr(point[4])

	while len(final_str)%8 > 0:
		final_str += '0'

	res = binStrToStr(final_str)
	res = bytes(res, 'utf-8')

	f = open(destination_filename, 'wb')
	f.write(res)
	f.close()


def strToComponents(s):
	i = 0

	n = binStrToInt(s[i:i+32])
	i += 32

	components = []

	for _ in range(0, n):
		x = binStrToInt(s[i:i+32])
		i += 32

		y = binStrToInt(s[i:i+32])
		i += 32
		
		bfs_str_len = binStrToInt(s[i:i+32])
		i += 32

		bfs_str = s[i:i+bfs_str_len]
		i += bfs_str_len

		components.append([x, y, bfs_str])

	m = binStrToInt(s[i:i+32])
	i += 32

	colored_points = []

	for _ in range(0, m):
		x = binStrToInt(s[i:i+32])
		i += 32

		y = binStrToInt(s[i:i+32])
		i += 32

		r = binStrToInt(s[i:i+32])
		i += 32

		g = binStrToInt(s[i:i+32])
		i += 32

		b = binStrToInt(s[i:i+32])
		i += 32

		colored_points.append([x, y, r, g, b])

	return components, colored_points


def con_decode(source_filename, destination_filename):
	f = open(source_filename, 'rb')
	s = f.read()
	s = str(s, 'UTF-8')
	f.close()

	s = strToBinStr(s)
	n = binStrToInt(s[0:32])
	m = binStrToInt(s[32:64])
	components, colored_points = strToComponents(s[64:])

	img = []

	for i in range(0, n):
		img.append([])
		for j in range(0, m):
			img[i].append([0, 0, 0])

	f = []

	for i in range(0, n):
		f.append([])
		for j in range(0, m):
			f[i].append(True)

	for component in components:
		x = component[0]
		y = component[1]
		bfs_str = component[2]

		r = 255
		g = 255
		b = 255
		
		a = [[x, y]]
		f[x][y] = False

		i = 0

		while len(a) > 0:
			x = a[0][0]
			y = a[0][1]
			f[x][y] = False

			a.pop(0)
			img[x][y] = [r, g, b]

			if bfs_str[i] == '1':
				a.append([x-1, y])
			i += 1

			if bfs_str[i] == '1':
				a.append([x+1, y])
			i += 1

			if bfs_str[i] == '1':
				a.append([x, y-1])
			i += 1

			if bfs_str[i] == '1':
				a.append([x, y+1])
			i += 1

	for point in colored_points:
		x = point[0]
		y = point[1]
		r = point[2]
		g = point[3]
		b = point[4]

		img[x][y] = [r, g, b]
		f[x][y] = False

		a = []
		a.append([x, y])

		while len(a) > 0:
			x = a[0][0]
			y = a[0][1]
			f[x][y] = False

			a.pop(0)
			img[x][y] = [r, g, b]

			if x-1 >= 0 and f[x-1][y]:
				a.append([x-1, y])
				f[x-1][y] = False
			if y-1 >= 0 and f[x][y-1]:
				a.append([x, y-1])
				f[x][y-1] = False
			if x+1 < n and f[x+1][y]:
				a.append([x+1, y])
				f[x+1][y] = False
			if y+1 < m and f[x][y+1]:
				a.append([x, y+1])
				f[x][y+1] = False

	for i in range(0, n):
		for j in range(0, m):
			img[i][j][2], img[i][j][0] = img[i][j][2], img[i][j][0]

	img = numpy.array(img)
	cv2.imwrite(destination_filename, img)



con_encode('SS3.bmp', 'SS0.bmp', 'con-compressed.dat')
con_decode('con-compressed.dat', 'recovered_intermediate.bmp')


