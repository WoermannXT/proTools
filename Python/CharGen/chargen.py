'''
Usage:
{1-99}
	[1, 2, 3 , ...]
{01-99}
	[01, 02, 03 , ...]
{0-1,a-b,C-D, x}
	[0, 1, a, b, C, D, x]
x{0-2}-{A-C}
	[x0-A, x0-B, x0-C, x1-A, x1-B, x1-C, x2-A, x2-B, x2-C]
1{c-d,m,n,o}-{1,2}
	[1c-1, 1c-2, 1d-1, 1d-2, 1m-1, 1m-2, 1n-1, 1n-2, 1o-1, 1o-2]
t {(tag)0-2}-{A-C}+[tag]
	[t 0-A+0, t 0-B+0, t 0-C+0, t 1-A+1, t 1-B+1, t 1-C+1, t 2-A+2, t 2-B+2, t 2-C+2]

ToDo:
	+Tags to reuse a variable
		{(tag)0-2}-{A-C}+[tag]
	-Escaping of special chars like {}(),-
'''

import re

dctCharTags = {}
rexp0 = re.compile(r"({(?:\((?P<tag>\w+)\))?(?P<grp_p>[^}]+)})") #find {x,,,}
rexp1 = re.compile(r"(?:(?P<grp_q>[^,]+),?)+?") #find x,,,
rexp2 = re.compile(r"(?P<grp_qp1>\d+)-(?P<grp_qp2>\d+)") #find 1-9
rexp3 = re.compile(r"(?P<grp_qp1>[a-zA-Z])-(?P<grp_qp2>[a-zA-Z])") #find a-z

def chargen(instr):
	global dctCharTags,rexp0,rexp1,rexp2,rexp3
	m = rexp0.search(instr)
	if m:
		tag = m.group(r'tag')
		mgrp_p = m.group(r'grp_p')
		m1 = rexp1.findall(mgrp_p)
		for gres in m1:
			if rexp2.match(gres): # numbers
				m2 = rexp2.match(gres)
				start = m2.group(r'grp_qp1')
				ende = int(m2.group(r'grp_qp2'))
				slen = len(start)
				start = int(start)
				for x in range(start, ende + 1):
					val = str(x).rjust(slen, '0')
					if tag:
						dctCharTags[tag] = val
					chargen(instr.replace(m.group(0), val, 1))
			elif rexp3.match(gres): # chars
				m3 = rexp3.match(gres)
				start = ord(m3.group(r'grp_qp1'))
				ende = ord(m3.group(r'grp_qp2'))
				for x in range(start, ende + 1):
					val = chr(x)
					chargen(instr.replace(m.group(0), val, 1))
			else:	# no increments, just value
				val = gres
				chargen(instr.replace(m.group(0), val, 1))
	else:
		for key, val in dctCharTags.items():
			instr = instr.replace('['+str(key)+']', val)
		print(instr) #-------------------------------------------------







