
'''
Simple Image Generator

'''

import argparse
import datetime
from random import *
from PIL import Image



def Worker(args):
	# -- Arguments Definitions --------------------------------------------------------------------------------------------------------------
	parser = argparse.ArgumentParser(description='FileMan Link Generator')
	# -- Size
	parser.add_argument('-x', '--width', default=255, type=int, help='Image width in pixels')
	parser.add_argument('-y', '--height', default=255, type=int, help='Image height in pixels')

	# -- Variable Definitions --------------------------------------------------------------------------------------------------------------
	args = parser.parse_args()
	# -- Initial Setup
	_w = args.width
	_h = args.height

	# -- Draw Image ------------------------------------------------------------------------------------------------------------------------
	img = Image.new( 'RGB', (_w,_h), "black") 
	pixels = img.load()
	for i in range(img.size[0]):
		for j in range(img.size[1]):
			pixels[i,j] = (i, j, 128)

	img.show()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		Worker(argv)
	except KeyboardInterrupt:
		pass
	#exit()
