'''
Usage:
'x{0-2}-{A-C}'
	['x0-A', 'x0-B', 'x0-C', 'x1-A', 'x1-B', 'x1-C', 'x2-A', 'x2-B', 'x2-C']
'1{c-d,m,n,o}-{1,2}'
	['1c-1', '1c-2', '1d-1', '1d-2', '1m-1', '1m-2', '1n-1', '1n-2', '1o-1', '1o-2']

'''

import re
import datetime

theList = []
#p = re.compile(r"(?P<grp_p>{[^}]+})") #find {x}
p = re.compile(r"({(?:\((?P<tag>\w+)\))?(?P<grp_p>[^}]+)})") #find {x,,,}
p1 = re.compile(r"(?:(?P<grp_q>[^,]+),?)+?") #find x,,,
p2 = re.compile(r"(?P<grp_qp1>\d+)-(?P<grp_qp2>\d+)") #find 1-9
p3 = re.compile(r"(?P<grp_qp1>[a-zA-Z])-(?P<grp_qp2>[a-zA-Z])") #find a-z
cnt = 0

def chargen(instr):
	global cnt
	tStart = datetime.datetime.now()
	# -----
	iterChars(instr)
	# -----
	tEnd = datetime.datetime.now()
	print(theList)
	print(tEnd-tStart)
	print(cnt)

def iterChars(instr):
	global theList,p,p1,p2,p3
	m = p.search(instr)
	if m:
		mgrp_p = m.group(r'grp_p')
		m1 = p1.findall(mgrp_p)
		for gres in m1:
			if p2.match(gres): # numbers
				m2 = p2.match(gres)
				start = m2.group(r'grp_qp1')
				ende = int(m2.group(r'grp_qp2'))
				slen = len(start)
				start = int(start)
				for x in range(start, ende + 1):
					val = str(x).rjust(slen, '0')
					iterChars(instr.replace(m.group(0), val, 1))
			elif p3.match(gres): # chars
				m3 = p3.match(gres)
				start = ord(m3.group(r'grp_qp1'))
				ende = ord(m3.group(r'grp_qp2'))
				for x in range(start, ende + 1):
					val = chr(x)
					iterChars(instr.replace(m.group(0), val, 1))
			else:	# no increments, just value
				val = gres
				iterChars(instr.replace(m.group(0), val, 1))
	else:
		resOutput(instr)

def resOutput(inStr):
	global cnt
	#print(inStr)
	cnt+=1
	theList.append(inStr)







