from utils import *


def encode(input_filename, destination_filename):
	# Read file
	img = Image.open(input_filename)
	img = numpy.array(img)

	n = len(img)
	m = len(img[0])

	components = []

	f = []

	for i in range(0, n):
		f.append([])
		for j in range(0, m):
			f[i].append(True)

	for i in range(0, n):
		for j in range(0, m):
			r = img[i][j][0]
			g = img[i][j][1]
			b = img[i][j][2]

			if r == 0 and g == 0 and b == 0:
				continue

			a = []

			a.append([i, j])
			img[i][j] = [0, 0, 0]

			color = (r*256*256)+(g*256)+b
			bfs_str = ''

			while len(a) > 0:
				x = a[0][0]
				y = a[0][1]

				a.pop(0)

				if x-1 >= 0 and (img[x-1][y][0] != 0 or img[x-1][y][1] != 0 or img[x-1][y][2] != 0) and almostEqualPixels([r, g, b], img[x-1][y], 1000):
					bfs_str += '1'
					a.append([x-1, y])
					img[x-1][y] = [0, 0, 0]
				else:
					bfs_str += '0'

				if x+1 < n and (img[x+1][y][0] != 0 or img[x+1][y][1] != 0 or img[x+1][y][2] != 0) and almostEqualPixels([r, g, b], img[x+1][y], 1000):
					bfs_str += '1'
					a.append([x+1, y])
					img[x+1][y] = [0, 0, 0]
				else:
					bfs_str += '0'

				if y-1 >= 0 and (img[x][y-1][0] != 0 or img[x][y-1][1] != 0 or img[x][y-1][2] != 0) and almostEqualPixels([r, g, b], img[x][y-1], 1000):
					bfs_str += '1'
					a.append([x, y-1])
					img[x][y-1] = [0, 0, 0]
				else:
					bfs_str += '0'

				if y+1 < m and (img[x][y+1][0] != 0 or img[x][y+1][1] != 0 or img[x][y+1][2] != 0) and almostEqualPixels([r, g, b], img[x][y+1], 1000):
					bfs_str += '1'
					a.append([x, y+1])
					img[x][y+1] = [0, 0, 0]
				else:
					bfs_str += '0'

			components.append([color, i, j, bfs_str])

	final_str = ''
	final_str += intToBinStr(n, 2)
	final_str += intToBinStr(m, 2)
	final_str += intToBinStr(len(components), 3)

	for component in components:
		final_str += intToBinStr(component[0], 3)
		final_str += intToBinStr(component[1], 3)
		final_str += intToBinStr(component[2], 3)
		final_str += intToBinStr(len(component[3]), 3)
		final_str += component[3]

	while len(final_str)%8 > 0:
		final_str += '0'

	res = binStrToStr(final_str)
	res = bytes(res, 'utf-8')

	f = open(destination_filename, 'wb')
	f.write(res)
	f.close()

