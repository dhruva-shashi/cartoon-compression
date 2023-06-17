from utils import *
from encoder import encode
from decoder import decode


crop = (117, 227, 1332, 909)

def compressImage():
	reduceColorsUsingKmeans('SS0.bmp', 'intermediate.bmp', 32)
	encode('intermediate.bmp', 'fully-compressed-2.dat')
	# decode('fully-compressed-2.dat', 'fully-recovered-2.bmp')


def bmpToJPEG():
	convertFormat('intermediate.bmp', 'SSp.jpg')


def bmpToPNG():
	convertFormat('SS0.bmp', 'SS0.png')


compressImage()
