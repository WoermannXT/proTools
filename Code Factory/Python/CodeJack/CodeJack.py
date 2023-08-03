#Generate CODE from Template
#CM_Types
#1	#actuator	Act	NULL	#sy.cm_type.control_module
#2	#special input	SpI	NULL	#sy.cm_type.control_module
#3	#counter	Cnt	NULL	#sy.cm_type.control_module
#4	#analog input	AnI	NULL	#sy.cm_type.control_module
#5	#polygon table	PoT	NULL	#sy.cm_type.control_module
#6	#universal value	UnV	NULL	#sy.cm_type.control_module
#7	#PID controller	PID	NULL	#sy.cm_type.control_module
#8	#message	Msg	NULL	#sy.cm_type.control_module
#9	#communication	Com	NULL	#sy.cm_type.control_module
#10	#frequence controller VLT	VLT	NULL	#sy.cm_type.control_module
#11	#frequence controller PFD	PFD	NULL	#sy.cm_type.control_module
#0	#pm.unit	Unit	NULL	#sy.cm_type.processunit
#12	#switch	Swi	NULL	#sy.cm_type.control_module
#30	#pm.tunit	TuS	NULL	#sy.cm_type.transferunit
#25	#equipment module	EM	NULL	#sy.cm_type.equipment_module
#40	#cm_type.vessel	Ves	NULL	#sy.cm_type.plc_globals

#Usage:
#python .\CodeGen.py -s ".\Templates\FB1{UnitNo_3}9E.awl" -d .\Output\ -p 1
#python .\CodeGen.py -s ".\Templates\FB1{UnitNo_3}9E.awl" -d P:\Bergen.Tine\GCLD\sim\ -p 3

import argparse
import datetime
import os
import pymssql
import unicodedata

def Worker(args):
	parser = argparse.ArgumentParser(description='FileMan Link Generator')
	parser.add_argument('-s', '--source', default='T:/WTR/', type=str, help='Source Template')
	parser.add_argument('-d', '--destination', default='D:/PS/', type=str, help='destination directory where links represent original files ad folders')
	parser.add_argument('-p', '--plc', default='1', type=str, help='PLC Number to create Blocks from')

	args = parser.parse_args()
	src = args.source
	dst = args.destination
	if dst[-1:]!="/" and dst[-1:]!="\\":
		dst=dst.replace("\\","/")+"/"
	plc = args.plc

	server = r'192.168.4.45\SK_BOTEC_DB'
	user = r'sa'
	password = r'delphi'
	db = r'KR_BERGEN_TINE_F1_Config'

	#Read Template --------------------------------------------------------------------------------------------
	tmpfile = open(src, "r")
	tmpdata = tmpfile.readlines()
	tmpfile.close()

	#Read Units (Sequesces) ---------------------------------------------------------------------------------------
	query = ('SELECT SY_BO_ENTITY.SEQUENCE_NO, SY_PLC.PLC_NO, SY_ENTITY.SYM_KR, SY_ENTITY.NAME '
			'FROM SY_BO_ENTITY INNER JOIN '
			'SY_ENTITY ON SY_BO_ENTITY.ENTITY_ID = SY_ENTITY.ENTITY_ID INNER JOIN '
			'SY_PLC ON SY_ENTITY.PLC_ID = SY_PLC.PLC_ID '
			'WHERE SY_PLC.PLC_NO = {} '
			'ORDER BY PLC_NO, SEQUENCE_NO'.format(plc))

	conn = pymssql.connect(server, user, password, db)
	cursor = conn.cursor()
	cursor.execute(query)
	for row in cursor:
		SeqNo = row[0]
		PLCNo = row[1]
		SYMU = row[2]
		NAME = row[3]
		print("PLC"+str(PLCNo).zfill(2)+" U"+str(SeqNo).zfill(3))
		#New FileName ---------------------------------------------------------------------------------------------
		dstd, file = os.path.split(os.path.abspath(src))
		file = file.replace("{UnitNo_3}",str(SeqNo).zfill(3)).replace("{UnitNo_2}",str(SeqNo).zfill(2)).replace("{UnitNo}",str(SeqNo)).replace("{UnitName}",str(NAME)).replace('{UnitSymbolic}',str(SYMU))
		newfilename = dst+"PLC"+str(PLCNo).zfill(2)+"/"+file#NAME.replace("#","")+".txt"
		newfilename = unicodedata.normalize('NFKD', newfilename).encode('ascii', 'ignore')
		dstd, file = os.path.split(os.path.abspath(newfilename))
		if not os.path.exists(dstd):
			os.makedirs(dstd)
		newfile = open(newfilename,'w')
		#Loop Through Lines ---------------------------------------------------------------------------------------
		myID = 0
		for index, line in enumerate(tmpdata):
			newline = line
			if "#" in newline[:2]:
				continue
			if "{UnitSymbolic}" in newline: newline = newline.replace('{UnitSymbolic}',str(SYMU))
			if "{UnitNo_3}" in newline: newline = newline.replace("{UnitNo_3}",str(SeqNo).zfill(3))
			if "{UnitNo_2}" in newline: newline = newline.replace("{UnitNo_2}",str(SeqNo).zfill(2))
			if "{UnitNo}" in newline: newline = newline.replace("{UnitNo}",str(SeqNo))
			if "{UnitName}" in newline: newline = newline.replace("{UnitName}",str(NAME))

			if getLabel(newline) == 'HEAD_PRESET': 
				myID = 0
				continue
			if getLabel(newline) == 'ACT_HEAD': 
				myID = 0
				continue
			if getLabel(newline) == 'ACT_PRESET_DATA': 
				myID = 1
				continue
			if getLabel(newline) == 'SPI_HEAD': 
				myID = 0
				continue
			if getLabel(newline) == 'SPI_PRESET_DATA': 
				myID = 2
				continue
			if getLabel(newline)== 'HEAD_READY': 
				myID = 0
				continue
			if getLabel(newline) == 'ACT_READY_DATA': 
				continue
			if getLabel(newline) == 'SPI_READY_DATA': 
				continue
			if getLabel(newline) == 'ANI_HEAD': 
				myID = 0
				continue
			if getLabel(newline) == 'VLT_HEAD': 
				myID = 0
				continue
			if getLabel(newline) == 'VLT_READY_DATA': 
				continue
			if getLabel(newline) == 'END_READY': 
				myID = 0
				continue
			if getLabel(newline) == 'HEAD_CIP': 
				myID = 0
				continue

			if getLabel(newline) == 'ANI_DATA': 
				myID = 4
				continue
			if getLabel(newline) == 'UNV_DATA': 
				myID = 6
				continue
			if getLabel(newline) == 'SPI_DATA': 
				myID = 2
				continue
			if getLabel(newline) == 'MSG_DATA': 
				myID = 8
				continue
			if getLabel(newline) == 'CNT_DATA': 
				myID = 3
				continue
			if getLabel(newline) == 'PID_DATA': 
				myID = 7
				continue
			if getLabel(newline) == 'VLT_DATA': 
				myID = 10
				continue
			if getLabel(newline) == 'ACT_DATA': 
				myID = 1
				continue
			if getLabel(newline) == 'REL_DATA': 
				myID = 1
				continue
			if getLabel(newline) == 'END': 
				myID = 0
				continue

			if getLabel(newline) is not None: 
				continue

			if "{CmSymbolic}" in newline and myID > 0: 
				query = ('SELECT SY_BO_ENTITY.SEQUENCE_NO, SY_PLC.PLC_NO, SY_CONTROL_MODULES.CM_TYPE_ID, SY_BO_ENTITY.ENTITY_ID, SY_CONTROL_MODULES.SYM_KR AS Expr1, SY_CONTROL_MODULES.DESC_PRIM_LANG, SY_CONTROL_MODULES.CM_NO '
				'FROM SY_BO_ENTITY INNER JOIN '
				'SY_CONTROL_MODULES ON SY_BO_ENTITY.ENTITY_ID = SY_CONTROL_MODULES.ENTITY_ID INNER JOIN '
				'SY_ENTITY ON SY_BO_ENTITY.ENTITY_ID = SY_ENTITY.ENTITY_ID AND SY_CONTROL_MODULES.ENTITY_ID = SY_ENTITY.ENTITY_ID INNER JOIN '
				'SY_PLC ON SY_ENTITY.PLC_ID = SY_PLC.PLC_ID '
				'WHERE SY_BO_ENTITY.SEQUENCE_NO = {} '
				'AND SY_PLC.PLC_NO = {} '
				'AND SY_CONTROL_MODULES.CM_TYPE_ID = {} '
				'ORDER BY PLC_NO, SEQUENCE_NO, CM_NO, CM_TYPE_ID'.format(SeqNo,PLCNo,myID))
				#print(query)

				conn2 = pymssql.connect(server, user, password, db)
				cursor2 = conn2.cursor()
				cursor2.execute(query)
				for row in cursor2:
					SeqNo = row[0]
					PLCNo = row[1]
					TYPE = row[2]
					ENTITY = row[3]
					SYMC = row[4]
					CMNO = row[5]
					newcm = newline.replace('{CmSymbolic}',str(SYMC))
					newfile.write(newcm)
					#print(newcm) #Only Info
				conn2.close()
			else:
				#print(newline) #Only Info
				newfile.write(newline)

			continue

		newfile.close()


	conn.close()
	exit()


	#f= open("_import.txt","w+")
	#f.close() 
	
	f=open("_LinkGen.txt", "a+")
	print("src = "+src+"; dst = "+dst)
	f.write("src = "+src+"; dst = "+dst+"\r\n")

	cntt=0
	tStart = datetime.datetime.now()
	f.write("Start:"+str(datetime.datetime.now())+"\r\n")
	for path, subdirs, files in os.walk(src):
		cnt=0
		for name in files:
			try:
				srcf=os.path.join(path, name)
				dstf=srcf.replace(src, dst)
				if os.path.isfile(dstf):
					print(dstf+" existing")
					continue
				dstd, xyz = os.path.split(os.path.abspath(dstf))
				if not os.path.exists(dstd):
					os.makedirs(dstd)
				os.symlink(srcf, dstf) #------------------------------
				cnt+=1
				cntt+=1
			except Exception as error:
				print(error)
				f.write("Error: "+str(error)+"\r\n")
		print(path+">"+str(cntt)+":"+str(cnt))

def getLabel(txtline):
	if txtline.find("[") >= 0: 
		label = txtline[txtline.find("[")+1:(txtline.find("]"))]
		return label

def getLableStruct(text, label):
	return ""



if __name__ == '__main__':
    from sys import argv
    try:
        Worker(argv)
    except KeyboardInterrupt:
        pass
exit()
