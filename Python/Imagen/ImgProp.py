
'''
Image Properies


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
import bson
import numpy



def Worker(args):
	print("User Current Version:-", sys.version)
	# -- Arguments Definitions --------------------------------------------------------------------------------------------------------------
	parser = argparse.ArgumentParser(description='FileMan Link Generator')
	# -- Size
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
	jd = {}

	# -- Image -----------------------------------------------------------------------------------------------------------------------------
	img = Image.open(_src) # Open Image
	tStart = datetime.datetime.now()
	jd = getImgProp(img)
#	jd['Prop'] = getProp(img)
	# JSON
	print(json.dumps(jd, indent=4))

	with open(_path + _fname + '_Prop.json', 'w', encoding='utf-8') as f:
		json.dump(jd, f, ensure_ascii=False, indent=4)

	# Ende
	tEnd = datetime.datetime.now()
	print(tEnd-tStart)

#------------------------------------------------------------------------------------
# Get EXIF Data ---------------------------------------------------------------------
# Returns NULL if no EXIF data available --------------------------------------------
def getImgProp(img):
	jd = {}
	jd['iPrp'] = {}
	jd['iPrp']['fmt'] = img.format
	jd['iPrp']['mod'] = img.mode
	jd['iPrp']['sze'] = img.size
	jd['iPrp']['pal'] = img.palette

	return jd

#------------------------------------------------------------------------------------
# Dict Clean up ---------------------------------------------------------------------
def dictcleaner(dct):
	if dct:
		for key, val in dct.items():
			if isinstance(val, dict):
				dct[key] = dictcleaner(val)
			elif isinstance(val, bytes):
				dct[key] = val.decode("utf-8", "ignore")  
	return dct

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		Worker(argv)
	except KeyboardInterrupt:
		pass
	exit()
