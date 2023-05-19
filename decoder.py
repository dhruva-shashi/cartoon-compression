from utils import *


def strToComponents(s):
	i = 0

	n = binStrToInt(s[i:i+24])
	i += 24

	components = []

	for _ in range(0, n):
		color = binStrToInt(s[i:i+24])
		i += 24

		x = binStrToInt(s[i:i+24])
		i += 24

		y = binStrToInt(s[i:i+24])
		i += 24
		
		bfs_str_len = binStrToInt(s[i:i+24])
		i += 24

		bfs_str = s[i:i+bfs_str_len]
		i += bfs_str_len

		components.append([color, x, y, bfs_str])

	return components


def decode(source_filename, destination_filename):
	f = open(source_filename, 'rb')
	s = f.read()
	s = str(s, 'UTF-8')
	f.close()

	s = strToBinStr(s)
	n = binStrToInt(s[0:16])
	m = binStrToInt(s[16:32])
	components = strToComponents(s[32:])

	img = []

	for i in range(0, n):
		img.append([])
		for j in range(0, m):
			img[i].append([0, 0, 0])

	for component in components:
		color = component[0]
		x = component[1]
		y = component[2]
		bfs_str = component[3]

		b = color%256
		color //= 256
		g = color%256
		color //= 256
		r = color%256
		
		a = [[x, y]]

		i = 0

		while len(a) > 0:
			x = a[0][0]
			y = a[0][1]

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


	for i in range(0, n):
		for j in range(0, m):
			img[i][j][2], img[i][j][0] = img[i][j][0], img[i][j][2]

	img = numpy.array(img)
	cv2.imwrite('recovered-intermediate.bmp', img)

	for i in range(0, n):
		prev = [0, 0, 0]
		for j in range(0, m):
			if img[i][j][0] != 0 or img[i][j][1] != 0 or img[i][j][2] != 0:
				prev[0] = img[i][j][0]
				prev[1] = img[i][j][1]
				prev[2] = img[i][j][2]

			img[i][j][0] = prev[0]
			img[i][j][1] = prev[1]
			img[i][j][2] = prev[2]

	cv2.imwrite(destination_filename, img)

