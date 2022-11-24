
'''
Simple Image Indexer


'''

import collections
import argparse
import datetime
import os
import sys
from io import BytesIO
from PIL import Image, ImageFile
import scipy.fftpack
import hashlib
import json
import numpy



def Worker(args):
	print("User Current Version:-", sys.version)
	# -- Arguments Definitions --------------------------------------------------------------------------------------------------------------
	parser = argparse.ArgumentParser(description='FileMan Link Generator')
	parser.add_argument('-s', '--source', type=str, default="./", help='Source Image File')
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
	size = (args.width, args.height)
	jd = {}

	# -- Image -----------------------------------------------------------------------------------------------------------------------------
	# ImageFile.LOAD_TRUNCATED_IMAGES = True # Check validity of this code line
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
	#-- Image Resize
	size = (8, 8)
	if aal:
		img2 = img.resize(size, Image.ANTIALIAS) #25s/10000 (depending on image size)
	else:
		img2 = img.resize(size,)

	size = (16, 16)
	if aal:
		img3 = img.resize(size, Image.ANTIALIAS) #25s/10000 (depending on image size)
	else:
		img3 = img.resize(size,)

	#-- 8x8 RGB Bitmap for Image Hash
	bmp = img2.tobytes()
	#print(bmp.decode('utf-16'))
	bmph = bmp.hex()
	#-- convert back to 64x3xFF
	#y = [bmph[i:i+6] for i in range(0, len(bmph), 6)]
	#for x, v in enumerate(y):
	#	y[x] = [v[i:i+2] for i in range(0, len(v), 2)]
	#print(' ---------------------------- ',y)
	#print(' ---------------------------- ',img2)
	#-- Save image to FS to see the result (only test) ------------
	#img2.save("./Test_8x8.bmp')
	
	#-- mapMD5
	imb = hashlib.md5(bmp)
	mapID = imb.hexdigest()
	
	h1= imghash(img2)
	h2= imghash2(img3)
	h3= mrfdhash(img3)
	h4= phash(img)
	print(h1)
	print(h2)
	print(h3)
	print(h4)
	#print('Rotation by %d: %d Hamming difference' % (r, h1 - h2))
	#-- visID
	visID = imghash(img2)
	#print(visID)
	#visID = imghash2(img2)
	#print(visID)
	#visID = myahash(img2)
	jd['visID'] = visID
	jd['mapID'] = mapID
	jd['map'] = bmph
	

	return jd

#------------------------------------------------------------------------------------
# Image (8x8) to Image Hash (Visual ID) ---------------------------------------------
# Returns 64 bit Hash String (16xhex) -----------------------------------------------
#------------------------------------------------------------------------------------
def imghash(img, size=8): # standard 64bit dHash, uses 8x8 image
	p=numpy.asarray(img).astype(numpy.int).sum(axis=2) # ravel is faster than flatten convert img to pixel array and sum rgb values and flatten
	p=numpy.append(p, p[0][0]) #add first pixel to end (65 pixel) for 64 bit
	d = p[1:] > p[:-1] #compare each pixel to the following one
	bs = ''.join(str(b) for b in 1 * d.flatten()) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)

def imghash2(img, size=8): # standard 64bit dHash, uses 16x16 image
	p=numpy.asarray(img).astype(numpy.int).reshape(16,8,6).sum(axis=2).reshape(8,2,8).sum(axis=1) # ravel is faster than flatten convert img to pixel array and sum rgb values and flatten
	p=numpy.append(p, p[0][0]) #add first pixel to end (65 pixel) for 64 bit
	d = p[1:] > p[:-1] #compare each pixel to the following one
	bs = ''.join(str(b) for b in 1 * d.flatten()) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)

def mrfdhash(img, size=8): # 64bit dHash: mirror, flip and rotation proof
	p=numpy.asarray(img).astype(numpy.int).sum(axis=2) #convert img to pixel array and sum rgb values
	p+=numpy.rot90(p)
	p=p[:size,:size]+numpy.flipud(p[size:,:size])+numpy.fliplr(p[:size,size:])+numpy.flipud(numpy.fliplr(p[size:,size:]))
	p=numpy.append(p, p[0][0]) #add first pixel to end (65 pixel) for 64 bit
	d = p[1:] > p[:-1] #compare each pixel to the following one
	bs = ''.join(str(b) for b in 1 * d.flatten()) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)

def phash(image, hash_size=8): #complex
	img_size = hash_size * 4
	image = image.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
	p = numpy.asarray(image)
	dct = scipy.fftpack.dct(scipy.fftpack.dct(p, axis=0), axis=1)
	dctlowfreq = dct[:hash_size, :hash_size]
	med = numpy.median(dctlowfreq)
	d = dctlowfreq > med
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
