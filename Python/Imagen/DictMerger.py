
'''
Dictionary Merger


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




def Worker(args):
	print("User Current Version:-", sys.version)
	jd1 = {'1':123, '2':234, '3':345, 'X':{'a':'abc', 'b':'bcd', 'c':'cde', }}
	jd2 = {'1':1234, '22':2234, '33':3345,  'X':{'aa':'aabc', 'bb':'bbcd', }}
	#jd = {**jd1, **jd2}

	print(jd1)
	print(jd2)
	jd = dctmrg(jd1, jd2)

	print(dictcleaner(jd))

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

#------------------------------------------------------------------------------------
# Dict Merger -----------------------------------------------------------------------
def dctmrg(dct,dctnew):
	for key, val in dctnew.items():
		if key in dct:
			if isinstance(val, dict):
				dct[key] = dctmrg(dct[key], dctnew[key])
			else:
				dct[key] = val
		else:
			dct[key] = dctnew[key]
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
