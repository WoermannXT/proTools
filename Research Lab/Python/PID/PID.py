
'''
PID Simulator and Optimizer
DS = DataSet

ds{x:{rnd:r, val:v, out:o, vac:c}}
x = data set number
r = random number
v = value raw (simulated)
o = pid output
c = value corrected by output
'''

import argparse
import datetime
from random import *
import matplotlib.pyplot as plt
from ValueSim import ValueSim


# -- Dictionary Definitions --------------------------------------------------------------------------------------------------------------
ds = {}
ds[0] = {'rnd':0, 'val':0, 'out':0, 'vac':0,}
ds[1] = {'rnd':0, 'val':0, 'out':0, 'vac':0,}
# PID Data Set
_kp = 0
_ki = 0
_kd = 0
pds = {'SetP':0.0, 'PVal':0.0, 'PVal1':0.0, 'OVal':0.0, 'dPV':0.0, 'E':0.0, 'kp':0.1, 'ki':0.01, 'kd':0.001, 'apw':1.0, }

def Worker(args):
	global ds, pds, _kp, _ki, _kd
	# -- Arguments Definitions --------------------------------------------------------------------------------------------------------------
	parser = argparse.ArgumentParser(description='FileMan Link Generator')
	# -- Initial Setup
	parser.add_argument('-ds', '--data_sets', default=100, type=int, help='Number of data sets')
	parser.add_argument('-it', '--iterations', default=10, type=int, help='Number of algorithm iterations')
	# -- PID Parameters
	parser.add_argument('-kp', '--prop_f', default=0.01, type=float, help='Factor proportional gain')
	parser.add_argument('-ki', '--integral_f', default=0.1, type=float, help='Factor integral gain')
	parser.add_argument('-kd', '--diff_f', default=0.001, type=float, help='Factor differential gain')
	# -- Value simulation parameters
	parser.add_argument('-vcr', '--value_change', default=1.0, type=float, help='Value change range / cycle')
	parser.add_argument('-vfi', '--value_filter', default=0.1, type=float, help='Value filter factor')
	parser.add_argument('-vnf', '--value_norm', default=0.999, type=float, help='Value normilization factor')
	parser.add_argument('-vds', '--value_dist', default=0.0, type=float, help='Value disturbance factor')
	# -- Value control parameters
	parser.add_argument('-apw', '--actuator_power', default=1.0, type=float, help='Actuator power x/1')
	parser.add_argument('-adt', '--actuator_dead_time', default=1.0, type=float, help='Actuator dead time delay in cycles')
	# -- Value control parameters
	parser.add_argument('-c', '--Config', default='Config.txt', type=str, help='Configuration File for S&R')

	# -- Variable Definitions --------------------------------------------------------------------------------------------------------------
	args = parser.parse_args()
	# -- Initial Setup
	_ds = args.data_sets
	#print('Number of data sets (-ds): ', _ds)
	_it = args.iterations
	#print('Number of algorithm iterations (-it): ', _it)
	# -- PID Parameters
	_kp = args.prop_f
	#print('Factor proportional gain (-kp): ', _kp)
	_ki = args.integral_f
	#print('Factor integral gain (-ki): ', _ki)
	_kd = args.diff_f
	#print('Factor proportional gain (-kd): ', _kd)
	# -- Value simulation parameters
	_vcr = args.value_change
	#print('Value change range / cycle (-vcr): ', _vcr)
	_vfi = args.value_filter
	#print('Value filter factor (-vfi): ', _vfi)
	_vnf = args.value_norm
	#print('Value normilization factor (-vnf): ', _vnf)
	_vds = args.value_dist
	#print('Value disturbance factor (-vds): ', _vds)
	# -- Value control parameters
	_apw = args.actuator_power
	#print('Actuator power x/1 (-apw): ', _apw)
	_adt = args.actuator_dead_time
	#print('Actuator dead time delay in cycles (-adt): ', _adt)



	# -- Initialize Dictionary --------------------------------------------------------------------------------------------------------------
	pds['kp'] = _kp
	pds['ki'] = _ki
	pds['kd'] = _kd
	ds = InitDS(ds, _ds,  _vcr, _vfi,)
	#print(ds[_ds-1])
	ds = ProcessDS(ds, _ds,  _vnf, _apw,)
	#print(ds[_ds-1])
	EvalDS(ds, _ds,)



	# -- Plot the graph ---------------------------------------------------------------------------------------------------------------------
	# x axis values
	#print(ds)
	x1 = []
	x2 = []
	y = []
	for key in ds:
		#print(ds[key]['val'])
		x1.append(ds[key]['val'])
		x2.append(ds[key]['out'])
		#print(key)
		y.append(key)
	# corresponding y axis values
	plt.plot(y,x1)
	plt.plot(y,x2)
	plt.show()

def InitDS(ds, dscnt, chnge, filt,):
	for p in range(2, dscnt):
		#VAL
		ds[p] = {'rnd':0, 'val':0, 'out':0, 'vac':0, }
		ds[p]['rnd'] = ValueSim(ds[p - 1]['rnd'], chnge, filt)
	return ds

def ProcessDS(ds, dscnt, norm, apw,):
	global pds
	for p in range(2, dscnt):
		#VAL
		ds[p]['val'] = (ds[p-1]['val'] + ds[p]['rnd'] + ( ds[p-1]['out'] - ds[p-2]['out'] ) * apw ) * norm
		#PID
		pds['PVal'] = ds[p]['val']
		pds['PVal1'] = ds[p-1]['val']
		pds = PID(pds)
		ds[p]['out'] =  pds['OVal']
	return ds


def EvalDS(ds, dscnt,):
	SumE = 0
	aaE = 0
	dirc = 0
	cnt = 0
	for p in range(2, dscnt):
		cnt += 1
		SumE += ds[p]['val']
		aaE += abs(ds[p]['val'])
		if ds[p]['val'] > ds[p - 1]['val'] < ds[p - 2]['val']:
			dirc +=1
		elif ds[p]['val'] < ds[p - 1]['val'] > ds[p - 2]['val']:
			dirc +=1

	aaE = aaE / cnt
	dirc = dirc/ cnt * 100
	print('         Error Sum: ', SumE)
	print('avg absolute error: ', aaE)
	print(' direction changes: ', dirc)


def Filter(val, val_old, alpha,):
 	return val * alpha + (val_old * (1.0 - alpha))



def PID(pds,):
	#PID Algorithm ----------------------------------------------------------------
	dPV = pds['PVal1'] - pds['PVal']
	E = pds['SetP'] - pds['PVal']
	#PID On -----------------------------------------------------------------------
	sPID = pds['kp'] * (E - pds['E'])		#Speed
	sPID += pds['ki'] * E					#Distance
	sPID += pds['kd'] * (dPV - pds['dPV'])		#Acceleration
	pds['OVal'] = pds['OVal'] + sPID
	#PID Finalise  ----------------------------------------------------------------
	pds['E'] = E
	pds['dPV'] = dPV
	return pds


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		Worker(argv)
	except KeyboardInterrupt:
		pass
	#exit()
