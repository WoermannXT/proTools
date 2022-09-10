
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
import string
from chargen import chargen

def ArgsMan(args):
	parser = argparse.ArgumentParser(description='Web The Ripper')
	#parser.add_argument('-s', '--source', default='This is the {0-99}th question: {a-z,A-Z,000-019,!,ü} - {000-999}', type=str, help='Source String')
	parser.add_argument('-s', '--source', default=' {(tag)0-2}-{A-C}+[tag]')

	args = parser.parse_args()
	s = args.source

	# -----
	chargen(s)
	# -----
	
#------------------------------------------------------------------------------------
# Main-------------------------------------------------------------------------------
if __name__ == '__main__':
    from sys import argv
    try:
        ArgsMan(argv)
    except KeyboardInterrupt:
        pass

