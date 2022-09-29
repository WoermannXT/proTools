
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

from ImgHash import getImgHash as ih
from ImgEXIF import getExif as exif
from DctTools import dctmrg as dm

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
	je = {}

	# -- Image Hash ------------------------------------------------------------------------------------------------------------------------
	img = Image.open(_src) # Open Image
	tStart = datetime.datetime.now()

	# srcMD5
	imb = hashlib.md5(_src.encode())
	srcID = imb.hexdigest()

	# rawMD5 3.5s/1000 !!! depending on file size very expensive
	imgb = img.tobytes()
	imb = hashlib.md5(imgb)
	rawID = imb.hexdigest()

	# -- Image EXIF ------------------------------------------------------------------------------------------------------------------------
	je['exif']= exif(img)

	# visID
	jih = ih(img, _aal)

	# -- JSON Dump--------------------------------------------------------------------------------------------------------------------------
	jd['vis'] = {jih['visID']:
					{'map':
						{jih['mapID']:
							{jih['map']:
								{'raw':
									{rawID:
										{
										'src':{srcID:_src},
										'exif':je['exif']
										}
									}
								}
							}
						}
					}
				}
	
	print(jd)
	print(json.dumps(jd, indent=4))
	with open(_path + _fname + '_Hash.json', 'w', encoding='utf-8') as f:
		json.dump(jd, f, ensure_ascii=False, indent=4)





	# Ende
	tEnd = datetime.datetime.now()
	print(tEnd-tStart)
	#img.show()
	#nfn = _fname + '_8x8.bmp'
	#img2.save(_path + nfn)

	



#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		Worker(argv)
	except KeyboardInterrupt:
		pass
	exit()
