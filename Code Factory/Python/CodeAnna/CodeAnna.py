'''
Read and Analyse Step 7 Code
'''

import argparse
import datetime
import re

x = {}	# Data Collector
b = {}	# Block Memory
 

#------------------------------------------------------------------------------------
# RegEx------------------------------------------------------------------------------

pat_block = r'''
(?P<type>FUNCTION_BLOCK|FUNCTION|ORGANIZATION_BLOCK)\s(?P<id>[^\n]+?)(:\s(?P<ret>[^\n]+?))?\n	# Block Start (FUNCTION "CIPTankCIPC" : VOID)
	(TITLE\s=(?P<titl>[^\r\n]+)\r?\n)	# Title (TITLE =CIP Tank CIP Control)
	(?P<comm>(//[^\r\n]+\r?\r\n)+)?					# Comments
	(AUTHOR\s:\s(?P<auth>[^\r\n]+)\r?\n)?		# Author (AUTHOR : Woermann)
	(FAMILY\s:\s(?P<fam>[^\r\n]+)\r?\n)?		# Family
	(NAME\s:\s(?P<name>[^\r\n]+)\r?\n)?			# Name (NAME : CIPUnitC)
	(VERSION\s:\s(?P<ver>[^\r\n]+)\r?\n)?		# Version (VERSION : 0.1)
	(.*?)		# Anything 
	(:?[\s\r\n]*VAR_INPUT\r?\n(?P<var_i>.+?)END_VAR\r?\n)?	# Input Varable Definitions
	(:?[\s\r\n]*VAR_OUTPUT\r?\n(?P<var_o>.+?)END_VAR\r?\n)?	# Output Varable Definitions
	(:?[\s\r\n]*VAR_IN_OUT\r?\n(?P<var_io>.+?)END_VAR\r?\n)?	# Input/Output Varable Definitions
	(:?[\s\r\n]*VAR\r?\n(?P<var>.+?)END_VAR\r?\n)?			# Stat Varable Definitions
	(:?[\s\r\n]*VAR_TEMP\r?\n(?P<var_t>.+?)END_VAR\r?\n)?		# Temporary (Local) Varable Definitions
	BEGIN(?P<code>.*)	# Block Code Begin
END_(?:FUNCTION_BLOCK|FUNCTION|ORGANIZATION_BLOCK|DATA_BLOCK|TYPE)	# Block End
'''
cpat_block = re.compile(pat_block, re.DOTALL | re.VERBOSE)
#------------------------------------------------------------------------------------

pat_netw = r'''
(?P<type>NETWORK).?\n	# Network Start
	(TITLE\s=(?P<titl>.+?)\s*\n)	# Title
	(?P<code>.*?)					# Network Code
(?=NETWORK|$)		# Block End
'''
cpat_netw = re.compile(pat_netw, re.DOTALL | re.VERBOSE)
#------------------------------------------------------------------------------------

pat_code = r'''
(?P<stmt>.*?;.*?\n)					# Statement line or block	
'''
cpat_code = re.compile(pat_code, re.DOTALL | re.VERBOSE)
#------------------------------------------------------------------------------------

pat_line = r'''
((?:)\s*\n)|
(\/+\s*(?P<cln>.+?)\s*\n)|
((?P<jds>[A-Za-z0-9_]+):)?\s+	# Jump Destination
(?P<cmd>[A-Z0-9*/+-=]+)\s+	# Command
(?P<val>[^;]+)?\s*		# Variable or operator
(?:;)\s*
(\/+\s*(?P<com>.+))?
'''
cpat_line = re.compile(pat_line, re.DOTALL | re.VERBOSE)

#------------------------------------------------------------------------------------
pat_call = r'''
^\s*(?P<id>[^\(\n/]+)\s*
(?:\(\n
(?P<val>[^\)]+)
\))?
'''
cpat_call = re.compile(pat_call, re.DOTALL | re.VERBOSE)

pat_dat = r"\s*(?P<id>[^:\s]+)\s*:=\s*(?P<val>[^,\n]+)"
cpat_dat = re.compile(pat_dat, re.DOTALL | re.VERBOSE)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# Argument Parser -------------------------------------------------------------------
def ArgsMan(args):
	parser = argparse.ArgumentParser(description='Regex Code Analysing Tool CodeAnna')
	parser.add_argument('-s', '--source', default='./file.awl', help='Source File to analyse.')

	args = parser.parse_args()
	srcFile = args.source

	tStart = datetime.datetime.now()
	# -----
	CodeAnna(srcFile)
	# -----
	tEnd = datetime.datetime.now()
	print(tEnd-tStart)

#------------------------------------------------------------------------------------
# CodeAnna---------------------------------------------------------------------------
def CodeAnna(file):
	try:
		# Try to open the file
		with open(file, "r") as file:
			contents = file.read()
	except FileNotFoundError:
		# Handle the error
		print("The file does not exist.")
		return

	BlockReader(contents)

def BlockReader(code):	# Block Reader (analyze content of Block)
	matches = cpat_block.finditer(code)
	for match in matches:
		b['blk'] = {}
		groups = match.groupdict()
		for name, value in groups.items():
			if not value is None:
				if name == "type":
					b['blk'][name] = value
				elif name == "id":
					b['blk'][name] = value
				elif name == "ret":
					b['blk'][name] = value
				elif name == "titl":
					b['blk'][name] = value
				elif name == "comm":
					b['blk'][name] = value
				elif name == "auth":
					b['blk'][name] = value
				elif name == "fam":
					b['blk'][name] = value
				elif name == "name":
					b['blk'][name] = value
				elif name == "ver":
					b['blk'][name] = value
				elif name == "var_i":
					b['blk'][name] = value
				elif name == "var_o":
					b['blk'][name] = value
				elif name == "var_io":
					b['blk'][name] = value
				elif name == "var":
					b['blk'][name] = value
				elif name == "var_t":
					b['blk'][name] = value
				elif name == "code":
					print(b)
					NetwReader(value)
				else:
					print("Unkown Group Name! {0}".format(str(value)))
		print(b['blk'])

def NetwReader(code):	# Network Reader (analyze content of Network)
	matches = cpat_netw.finditer(code)
	b['nwk'] = {}
	for match in matches:
		groups = match.groupdict()
		for name, value in groups.items():
			if not value is None:
				if name == "type":
					b['nwk'][name] = value
				elif name == "titl":
					b['nwk'][name] = value
				elif name == "code":
					CodeReader(value)
				else:
					print("Unkown Group Name! {0}".format(str(value)))
	print(b['nwk'])

def CodeReader(code):	# Code Reader (analyze Code by statement)
	matches = cpat_code.finditer(code)
	for match in matches:
		groups = match.groupdict()
		for name, value in groups.items():
			if not value is None:
				LineReader(value)

def LineReader(code):	# Line Reader (analyze Code Line by Line)
	matches = cpat_line.finditer(code)
	#for g in matches:
		#print(g.group("name"), " --> ", g.group("val"))
		#StmtInterpreter(g)
	for match in matches:
		groups = match.groupdict()
		StmtInterpreter(groups)

def StmtInterpreter(dict):	#Analyse each code line
	for name, value in dict.items():
		if not value is None:
			if name == 'cmd' and value == 'CALL': 		# Find all Block Calls
				CallAnalyser(dict['val'])
			elif name == 'cln': 		# Find all Comment Lines
				print("This is a comment line: ", value)

def CallAnalyser(code):	# Analyse a CALL and its Parameters
	match = cpat_call.search(code)
	blk=re.sub('"', '', match.group("id").lower())
	print(blk)
	if match.group("val"):
		res = cpat_dat.finditer(match.group("val"))
		v = {}
		for g in res:
			v[g.group("id")] = g.group("val")
		print(v)





#------------------------------------------------------------------------------------
# Main-------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		ArgsMan(argv)
	except KeyboardInterrupt:
		pass
