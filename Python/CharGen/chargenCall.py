
"""
Generate series of chars fom start char to end char
	or of a given selection of chars
	chars are based on the 255 ASCII Table

definition is inside {}:
	{1-99}; {a-z}; {2002-2022}; {2,4,6,8,00-99} {0-9,a-z,A-Z}

hexadecimal digits would be:
	{0-9,a-f} or {0-9,A-F}

formats are defined by the input:
	{000-128}

"""


import argparse
import datetime
from chargen import chargen

def ArgsMan(args):
	parser = argparse.ArgumentParser(description='Web The Ripper')
	parser.add_argument('-i', '--input', default=' {(tag)0-2}-{A-C}+[tag]')

	args = parser.parse_args()
	s = args.input

	tStart = datetime.datetime.now()
	# -----
	chargen(s)
	# -----
	tEnd = datetime.datetime.now()
	print(tEnd-tStart)
	
def worker(instr):
	print(instr)



#------------------------------------------------------------------------------------
# Main-------------------------------------------------------------------------------
if __name__ == '__main__':
    from sys import argv
    try:
        ArgsMan(argv)
    except KeyboardInterrupt:
        pass

