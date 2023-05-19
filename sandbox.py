from utils import *
from encoder import encode
from decoder import decode
from generate_intermediate import generateIntermediate


crop = (117, 227, 1332, 909)

def compressImage():
	encode('intermediate.bmp', 'fully-compressed.dat')
	decode('fully-compressed.dat', 'fully-recovered.bmp')


def bmpToJPEG():
	convertFormat('SS0.bmp', 'SS0.jpg')


def bmpToPNG():
	convertFormat('SS0.bmp', 'SS0.png')


compressImage()


