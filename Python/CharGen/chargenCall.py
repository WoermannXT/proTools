
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

