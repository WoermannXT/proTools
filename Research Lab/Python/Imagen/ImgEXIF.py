
'''
EXIF Data Extractor


'''

import collections
import argparse
import datetime
import os
import sys
from io import BytesIO
from PIL import Image
import hashlib
import pickle
import json
#import exifread

from DctTools import dctcln


def Worker(args):
	print("User Current Version:-", sys.version)
	# -- Arguments Definitions --------------------------------------------------------------------------------------------------------------
	parser = argparse.ArgumentParser(description='FileMan Link Generator')
	parser.add_argument('-s', '--source', type=str, help='Source Image File')

	# -- Variable Definitions --------------------------------------------------------------------------------------------------------------
	args = parser.parse_args()
	# -- Initial Setup
	_src = args.source
	_fso = os.path.split(_src)
	_path = _fso[0] + '/'	#Folder / Path
	_file = _fso[1]			#Filename with Extension
	_fob = os.path.splitext(_file)
	_fname = _fob[0]		#Filename (without Extension)
	_fext = _fob[1]			#File Extension (.txt)
	
	dct = {}

	# -- Image -----------------------------------------------------------------------------------------------------------------------------
	img = Image.open(_src) # Open Image
	tStart = datetime.datetime.now()
	
	#img = open(_src, "rb") # -- test exifread

	dct['EXIF'] = getExif(img)

	print(dct)
	# JSON
	print(json.dumps(dct, indent=4, sort_keys=True))

	with open(_path + _fname + '_EXIF.pckl', 'wb') as f:
		pickle.dump(dct, f)

	with open(_path + _fname + '_EXIF.json', 'w', encoding='utf-8') as f:
		json.dump(dct, f, ensure_ascii=False, indent=4)

	# Ende
	tEnd = datetime.datetime.now()
	print(tEnd-tStart)

#------------------------------------------------------------------------------------
# Get EXIF Data ---------------------------------------------------------------------
# Returns NULL if no EXIF data available --------------------------------------------
def getExif(img):
	exif = img._getexif()
	#exif = exifread.process_file(img)
	if exif:
		#print(exif)
		# Clean EXIF Data:
		# CFAPattern 	41730 	0xA302 	ExifUndefined 	byte[]
		# DeviceSettingDescription 	41995 	0xA40B 	ExifUndefined 	byte[]
		
		#? ComponentsConfiguration 	37121 	0x9101 	ExifUndefined 	byte[4]
		# ZerothIFDPadding 	59932 	0xEA1C 	ExifUndefined 	byte[]
		# PrintIM;PrintImageMatching 	50341	0xc4a5 	IFD0 	undef 	--> PrintIM Tags
		# 50898
		# 50899
		keys = [37121,50341,50898,50899,59932] #delete
		for key in keys:
			if key in exif: 
				exif.pop(key)
				print("Key {key} deleted!".format(key = key))
		# MakerNote 	37500 	0x927C 	ExifUndefined 	byte[]
		# UserComment 	37510 	0x9286 	ExifEncodedString 	string
		keys = [37500,37510] # Unicode Decode
		for key in keys:
			if key in exif: 
				v = exif[key]
				if type(v) == bytes:
					#v = v.decode('utf-16', "ignore") 
					v = v.replace(b'\x00\x00',b'')
				elif type(v) == str:
					v = v.replace('\x00\x00','')
				exif[key] = v
	return dctcln(exif)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		Worker(argv)
	except KeyboardInterrupt:
		pass
	exit()
