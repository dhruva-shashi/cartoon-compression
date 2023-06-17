from utils import *


def strToQuad(s):
	res = 0

	if s[0] == '1':
		res += 2
	if s[1] == '1':
		res += 1

	return chr(res+ord('0'))


def strToChar(s):
	res = 0

	if s[0] == '1':
		res += 8
	if s[1] == '1':
		res += 4
	if s[2] == '1':
		res += 2
	if s[3] == '1':
		res += 1

	if res < 10:
		return chr(res+ord('0'))

	return chr(res-10+ord('A'))


def convertToHex(s):
	n = len(s)

	i = 0

	res = ''

	while i < n:
		res += strToChar(s[i:i+4])
		i += 4

	return res


def convertToQuad(s):
	n = len(s)

	i = 0

	res = ''

	while i < n:
		res += strToQuad(s[i:i+2])
		i += 2

	return res


def convertToBin(s):
	n = len(s)
	res = []

	for i in range(0, n):
		res.append(s[i])

	return res


def bwt(s):
	n = len(s)

	a = []

	for i in range(0, n):
		a.append(s[i])

	arr = []

	for i in range(0, n):
		a.append(a[0])
		a.pop(0)
		arr.append([a.copy(), i])

	arr.sort()

	pos = -1

	for i in range(0, n):
		if arr[i][1] == n-1:
			pos = i

	res = []

	for i in range(0, n):
		res.append(arr[i][0][n-1])

	return res, pos


def bwtInverse(s, index):
	n = len(s)

	a = []

	for i in range(0, n):
		a.append([])

	for i in range(0, n):
		for j in range(0, n):
			a[j].insert(0, s[j])

		a.sort()

	return a[index]


def longStrBwt(s):
	while len(s)%512 != 0:
		s += '0'

	new_str = convertToQuad(s)
	n = len(new_str)

	bwt_str = ''
	pos_arr = []

	for i in range(0, n, 256):
		c = new_str[i:i+256]
		e, f = bwt(c)

		for g in e:
			bwt_str += g

		pos_arr.append(f)

	return bwt_str, pos_arr


def mtf(s):
	n = len(s)

	x = ['0', '1', '2', '3']

	res = ''

	for i in range(0, n):
		for j in range(0, 4):
			if x[j] == s[i]:
				x.pop(j)
				x.insert(0, s[i])
				res += chr(j+ord('0'))
				break

	return res


def mtfInverse(s):
	n = len(s)

	x = ['0', '1', '2', '3']

	res = ''

	for i in range(0, n):
		y = ord(s[i])-ord('0')
		ch = x[y]
		res += ch
		x.pop(y)
		x.insert(0, ch)

	return res


def quadStrToBin(s):
	n = len(s)

	res = ''

	for i in range(0, n):
		if s[i] == '0':
			res += '00'
		if s[i] == '1':
			res += '01'
		if s[i] == '2':
			res += '10'
		if s[i] == '3':
			res += '11'

	return res


def sixBitsToBinStr(num):
	res = ''

	while num:
		res += chr(ord('0')+num%2)
		num //= 2

	res.reverse()
	return res


def rle(s):
	n = len(s)
	i = 0

	res = ''

	while i < n:
		k = 0
		j = i

		while i < n and s[j] == s[i] and k < 63:
			k += 1
			i += 1

		if s[j] == '0':
			res += '00'
		if s[j] == '1':
			res += '01'
		if s[j] == '2':
			res += '10'
		if s[j] == '3':
			res += '11'

		res += sixBitsToBinStr(k)

	return res


def compress(s):
	bwt_res, pos_arr = longStrBwt(s)
	mtf_res = mtf(bwt_res)

	res = intToBinStr(len(mtf_res), 4)

	res += rle(mtf_res)

	for pos in pos_arr:
		res += intToBinStr(pos, 1)

	return res

def decompress(s, pos_arr):
	bwt_res = mtfInverse(s)
	

s = '01001001001011011111111101001010'
res = compress(s)
print(len(res))




	


