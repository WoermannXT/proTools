
'''
Simple Image Indexer


'''

import collections
import argparse
from datetime import datetime
import os
import sys
from io import BytesIO
from PIL import Image, ImageFile
import scipy.fftpack
import hashlib
import json
import numpy
import matplotlib.pyplot as plt


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
	#size = (args.width, args.height)
	jd = {}

	# -- Image -----------------------------------------------------------------------------------------------------------------------------

	if os.path.isdir(_src):
		for file_name in _src:
			imgLoad(os.path.join(_src, file_name), _aal)
	elif os.path.isfile(_src):
		imgLoad(_src, _aal)
	else:
		print(f"{_src} is neither a file nor a directory.")

def imgLoad(_src, _aal):
	# ImageFile.LOAD_TRUNCATED_IMAGES = True # Check validity of this code line
	img = Image.open(_src) # Open Image
	tStart = datetime.now()

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
	#with open(_path + _fname + '_Hash.json', 'w', encoding='utf-8') as f:
	#	json.dump(jd, f, ensure_ascii=False, indent=4)

	# Ende
	tEnd = datetime.now()
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
		img2 = img.resize(size, Image.Resampling.LANCZOS) #25s/10000 (depending on image size), Image.Resampling.LANCZOS
	else:
		img2 = img.resize(size,)

	size = (16, 16)
	if aal:
		img3 = img.resize(size, Image.Resampling.LANCZOS) #25s/10000 (depending on image size)
	else:
		img3 = img.resize(size,)

	size = (32, 32)
	if aal:
		img4 = img.resize(size, Image.Resampling.LANCZOS) #25s/10000 (depending on image size)
	else:
		img4 = img.resize(size,)

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
	start = datetime.utcnow()
	for i in range(0,9999):
		h8= phashorg(img)
	print('p-h--', datetime.utcnow()-start, h8)


	start = datetime.utcnow()
	for i in range(0,9999):
		h11= phashorg(img, 6)
	print('p-h-6', datetime.utcnow()-start, h11)


	start = datetime.utcnow()
	for i in range(0,9999):
		h12= p_hash(img4.convert("L"))#phash(img)
	print('p-h1-', datetime.utcnow()-start, h12[64])
	print('p-h2-', datetime.utcnow()-start, h12[32])


	start = datetime.utcnow()
	for i in range(0,9999):
		h7= rf_hash(img4.convert("L"))#phash(img)
	print('rfh1-', datetime.utcnow()-start, h7[64])
	print('rfh2-', datetime.utcnow()-start, h7[32])


	start = datetime.utcnow()
	for i in range(0,9999):
		h1= s_hash(img4.convert("L"))
	print('s-h1-', datetime.utcnow()-start, h1[64])
	print('s-h2-', datetime.utcnow()-start, h1[32])


	#print('Rotation by %d: %d Hamming difference' % (r, h1 - h2))
	#-- visID
	visID = h8
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
def p_hash(image):		 	# 32x32 greyscale image -----------------------------------------------------
	jd={}
	pix=numpy.asarray(image)
	dct = scipy.fftpack.dct(scipy.fftpack.dct(pix, axis=0), axis=1)
	dctlowfreq64 = dct[:8, :8]
	dctlowfreq36 = dct[:6, :6]
	med = numpy.median(dctlowfreq64)
	diff = dctlowfreq64 > med
	bit_string = ''.join(str(b) for b in 1 * diff.flatten()) #convert array to a bit string
	width = int(numpy.ceil(len(bit_string)/4)) #length of hash
	jd[64]='{:0>{width}x}'.format(int(bit_string, 2), width=width)
	med = numpy.median(dctlowfreq36)
	diff = dctlowfreq36 > med
	diff = diff.flatten()
	bit_string = ''.join(str(b) for b in 1 * diff[:-4]) #convert array to a bit string
	width = int(numpy.ceil(len(bit_string)/4)) #length of hash
	jd[32]='{:0>{width}x}'.format(int(bit_string, 2), width=width)
	return jd

def rf_hash(img): 			# 32x32 greyscale image -----------------------------------------------------
	jd={}
	pix=numpy.asarray(img).reshape(16, 2, 16, 2).sum(axis=(1, 3))	# Sum up the colour values (3d to 2d)
	pix=pix+numpy.rot90(pix)	# add a 90° rotated array to the original
	pix=pix+numpy.flipud(pix)+numpy.fliplr(pix)+numpy.flipud(numpy.fliplr(pix))	+1 #add the 1 to detect black values (0,0,0)
	pix=numpy.triu(pix) # remove bottom triangle from array (size = (16*16)/2+16=144)
	pix=pix[pix != 0]	#flatten and remove zeros (size = (16*16)/2+16=144)
	pix=pix.reshape(-1, 2).sum(axis=1)	# Get Arr for 64 bit hash (144/2=144)
	pix2=pix.reshape(-1, 2).sum(axis=1)	# Get Arr for 32 bit hash
	pix=pix[3:]	# Cut of first 3 values to get 65 Vals -> 64 bits
	diff = pix[1:] > pix[:-1]
	bit_string = ''.join(str(b) for b in 1 * diff)
	width = int(numpy.ceil(len(bit_string)/4))
	jd[64]='{:0>{width}x}'.format(int(bit_string, 2), width=width)
	pix2=pix2[1:]	# Cut of first value
	diff = pix2[1:] > pix2[:-1]
	bit_string = ''.join(str(b) for b in 1 * diff)
	width = int(numpy.ceil(len(bit_string)/4))
	jd[32]='{:0>{width}x}'.format(int(bit_string, 2), width=width)
	return jd

def s_hash(img):			# 32x32 greyscale image -----------------------------------------------------
	jd={}
	pix=numpy.asarray(img).reshape(8, 4, 8, 4).sum(axis=(1, 3))	# Sum up the colour values (3d to 2d)
	pix2=pix.reshape(-1, 2).sum(axis=1)	# Get Arr for 32 bit hash
	pix=numpy.append(pix, pix[0][0]) #add first pixel to end (65 pixel) for 64 bit
	diff = pix[1:] > pix[:-1] #compare each pixel to the following one
	bit_string = ''.join(str(b) for b in 1 * diff.flatten()) #convert array to a bit string
	width = int(numpy.ceil(len(bit_string)/4)) #length of hash
	jd[64]='{:0>{width}x}'.format(int(bit_string, 2), width=width)
	pix2=numpy.append(pix2, pix2[0]) #add first pixel to end (33 pixel) for 32 bit
	diff = pix2[1:] > pix2[:-1] #compare each pixel to the following one
	bit_string = ''.join(str(b) for b in 1 * diff.flatten()) #convert array to a bit string
	width = int(numpy.ceil(len(bit_string)/4)) #length of hash
	jd[32]='{:0>{width}x}'.format(int(bit_string, 2), width=width)
	return jd








def imghash8(img, size=8): # standard 64bit dHash, uses 8x8 image
	p=numpy.asarray(img).sum(axis=2) # ravel is faster than flatten convert img to pixel array and sum rgb values and flatten
	p=numpy.append(p, p[0][0]) #add first pixel to end (65 pixel) for 64 bit
	d = p[1:] > p[:-1] #compare each pixel to the following one
	bs = ''.join(str(b) for b in 1 * d.flatten()) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)

def imghash16(img, size=8): # standard 64bit dHash, uses 16x16 image
	p=numpy.asarray(img).reshape(16,8,6).sum(axis=2).reshape(8,2,8).sum(axis=1) # ravel is faster than flatten convert img to pixel array and sum rgb values and flatten
	p=numpy.append(p, p[0][0]) #add first pixel to end (65 pixel) for 64 bit
	d = p[1:] > p[:-1] #compare each pixel to the following one
	bs = ''.join(str(b) for b in 1 * d.flatten()) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)

def mrfdhash(img, size=8): # 64bit dHash: mirror, flip and rotation proof
	p=numpy.asarray(img).sum(axis=2) #convert img to pixel array and sum rgb values
	p+=numpy.rot90(p)
	p=p[:size,:size]+numpy.flipud(p[size:,:size])+numpy.fliplr(p[:size,size:])+numpy.flipud(numpy.fliplr(p[size:,size:]))
	p=numpy.append(p, p[0][0]) #add first pixel to end (65 pixel) for 64 bit
	d = p[1:] > p[:-1] #compare each pixel to the following one
	bs = ''.join(str(b) for b in 1 * d.flatten()) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)

def rf_hash64(img): # Image size must be 32x32 rgb -----------------------------------------------------
	#numpy.asarray(img): convert image to numpy array
	#astype(numpy.int): convert ti type INT
	#sum(axis=2): sum up the rgb values
	#reshape(16, 2, 16, 2).sum(axis=(1, 3)): reschape to a 16x16 array
	pix=numpy.asarray(img).sum(axis=2).reshape(16, 2, 16, 2).sum(axis=(1, 3))	# Sum up the colour values (3d to 2d)
	pix=pix+numpy.rot90(pix)	# add a 90° rotated array to the original
	pix=pix+numpy.flipud(pix)+numpy.fliplr(pix)+numpy.flipud(numpy.fliplr(pix))	+1 #add the 1 to detect black values (0,0,0)
	pix=numpy.triu(pix) # remove bottom triangle from array
	pix=pix[pix != 0]	#flatten and remove zeros
	pix=pix.reshape(-1, 2).sum(axis=1)
	pix=pix[3:]
	diff = pix[1:] > pix[:-1]
	bit_string = ''.join(str(b) for b in 1 * diff)
	width = int(numpy.ceil(len(bit_string)/4))
	return '{:0>{width}x}'.format(int(bit_string, 2), width=width)

def rf_hash32(img): # Image size must be 32x32 rgb -----------------------------------------------------
	pix=numpy.asarray(img).sum(axis=2).reshape(16, 2, 16, 2).sum(axis=(1, 3))	# Sum up the colour values (3d to 2d)
	pix=pix+numpy.rot90(pix)	# add a 90° rotated array to the original
	pix=pix+numpy.flipud(pix)+numpy.fliplr(pix)+numpy.flipud(numpy.fliplr(pix))	+1 #add the 1 to detect black values (0,0,0)
	pix=numpy.triu(pix) # remove bottom triangle from array
	pix=pix[pix != 0]	#flatten and remove zeros
	pix=pix.reshape(-1, 2).sum(axis=1)
	pix=pix.reshape(-1, 2).sum(axis=1)
	pix=pix[1:]
	diff = pix[1:] > pix[:-1]
	bit_string = ''.join(str(b) for b in 1 * diff)
	width = int(numpy.ceil(len(bit_string)/4))
	return '{:0>{width}x}'.format(int(bit_string, 2), width=width)



def phashorg(image, hash_size=8):
	img_size = hash_size * 4
	image = image.convert("L").resize((img_size, img_size), Image.Resampling.LANCZOS)
	p = numpy.asarray(image)
	dct = scipy.fftpack.dct(scipy.fftpack.dct(p, axis=0), axis=1)
	dctlowfreq = dct[:hash_size, :hash_size]
	med = numpy.median(dctlowfreq)
	d = dctlowfreq > med
	bs = ''.join(str(b) for b in 1 * d.flatten()) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)




def phash64(image): # 32x32 greyscale image
	#p=numpy.asarray(image).astype(int).sum(axis=2)	# Sum up the colour values (3d to 2d)
	p=numpy.asarray(image)	# Sum up the colour values (3d to 2d)
	#print('size:', p.size)
	dct = scipy.fftpack.dct(scipy.fftpack.dct(p, axis=0), axis=1)
	#print('size:', dct.size)
	dctlowfreq = dct[:8, :8]
	#print('size:', dctlowfreq.size)
	med = numpy.median(dctlowfreq)
	#print('size:', med.size)
	d = dctlowfreq > med
	#print('5.', d, 'size:', d.size)
	bs = ''.join(str(b) for b in 1 * d.flatten()) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)

def phash32(image): #complex
	#p=numpy.asarray(image).astype(int).sum(axis=2)	# Sum up the colour values (3d to 2d)
	p=numpy.asarray(image).sum(axis=2)	# Sum up the colour values (3d to 2d)
	#print('size:', p.size)
	dct = scipy.fftpack.dct(scipy.fftpack.dct(p, axis=0), axis=1)
	#print('size:', dct.size)
	dctlowfreq = dct[:6, :6]
	#print('size:', dctlowfreq.size)
	med = numpy.median(dctlowfreq)
	#print('size:', med.size)
	d = dctlowfreq > med
	d = d.flatten()
	bs = ''.join(str(b) for b in 1 * d[:-4]) #convert array to a bit string
	l = int(numpy.ceil(len(bs)/4)) #length of hash
	return '{:0>{l}x}'.format(int(bs, 2), l=l)

# Compute the Hamming distance between the Hash values to determine the similarity between the images
def ham_dist(h1, h2):
	return bin(h1 ^ h2).count('1')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		Worker(argv)
	except KeyboardInterrupt:
		pass
	exit()
