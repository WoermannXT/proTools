
'''
Simple Image Indexer


'''

import collections
import argparse
import datetime
import os
import sys
from io import BytesIO
from PIL import Image
import hashlib
import json
import numpy



def Worker(args):
	print("User Current Version:-", sys.version)
	# -- Arguments Definitions --------------------------------------------------------------------------------------------------------------
	parser = argparse.ArgumentParser(description='FileMan Link Generator')
	parser.add_argument('-s', '--source', type=str, help='Source Image File')
	parser.add_argument('-a', '--antialias', action='store_true', help='Image height in pixels')

	# -- Variable Definitions --------------------------------------------------------------------------------------------------------------
	args = parser.parse_args()
	# -- Initial Setup
	_src = args.source
	_aal = args.antialias

	_fso = os.path.split(_src)
	_path = _fso[0] + '/'	#Folder / Path
	_file = _fso[1]			#Filename with Extension
	_fob = os.path.splitext(_file)
	_fname = _fob[0]		#Filename (without Extension)
	_fext = _fob[1]			#File Extension (.txt)
	#size = (args.width, args.height)
	jd = {}

	# -- Image -----------------------------------------------------------------------------------------------------------------------------
	img = Image.open(_src) # Open Image
	tStart = datetime.datetime.now()

	jd = getImgHash(img, _aal)
	
	# srcMD5
	imb = hashlib.md5(_src.encode())
	srcID = imb.hexdigest()
	jd['srcMD5'] = srcID
	jd['src'] = _src
	
	# rawMD5 3.5s/1000 !!! depending on file size very expensive
	imgb = img.tobytes()
	imb = hashlib.md5(imgb)
	rawID = imb.hexdigest()
	jd['rawMD5'] = rawID

	# JSON
	print(json.dumps(jd, indent=4))
	with open(_path + _fname + '_Hash.json', 'w', encoding='utf-8') as f:
		json.dump(jd, f, ensure_ascii=False, indent=4)

	# Ende
	tEnd = datetime.datetime.now()
	print(tEnd-tStart)
	#img.show()
	#nfn = _fname + '_8x8.bmp'
	#img2.save(_path + nfn)


#------------------------------------------------------------------------------------
# get Image Hash --------------------------------------------------------------------
#------------------------------------------------------------------------------------
def getImgHash(img, aal):
	jd = {}
	# Image Resize
	size = (8, 8)
	if aal:
		img2 = img.resize(size, Image.ANTIALIAS) #25s/10000 (depending on image size)
	else:
		img2 = img.resize(size,)

	# 8x8 RGB Bitmap for Image Hash
	bmp = img2.tobytes()
	bmph = bmp.hex()

	# mapMD5
	imb = hashlib.md5(bmp)
	mapID = imb.hexdigest()
	
	# visID
	visID = imghash(img2)
	jd['visID'] = visID
	jd['mapID'] = mapID
	jd['map'] = bmph

	return jd

#------------------------------------------------------------------------------------
# Image (8x8) to Image Hash (Visual ID) ---------------------------------------------
# Returns 64 bit Hash String (16xhex) -----------------------------------------------
#------------------------------------------------------------------------------------
def imghash(img):
	p=numpy.asarray(img).astype(numpy.int).sum(axis=2).ravel() #convert img to pixel array and sum rgb values and flatten
	p=numpy.append(p, p[0]) #add first pixel to end (65 pixel) for 64 bit
	d = p[1:] > p[:-1] #compare each pixel to the following one
	bs = ''.join(str(b) for b in 1 * d.flatten()) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		Worker(argv)
	except KeyboardInterrupt:
		pass
	exit()
