
'''
Value Simulator

Initial Value = ???

Frequency Partitions:
Each Partition consists of an 
	- Oscilator
		Period = Period of sinus curve
		Amplitude = Amplitude of Sinus curve
	- Randomizer
		Gain = Factor for random sum addition
		Pull = Factor to pull the value towards 0 (Gravitator)
	- Filter
		Alpha
		Min
		Max
High Frequency Partition (HFP)
Medium Frequency Partition (MFP)
Low Frequency Partition (LFP)

Value = Value + HFP + MFP + LFP








-vcr	--value_change	default=1.0, type=float, 	Value change range / cycle
-fis	--filter_std	default=0.1, type=float, 	Filter Standard Factor
-fcr	--filter_change	default=0.1, type=float, 	Filter change range / cycle
-vnf	--value_norm	default=0.9999, type=float, Value normilization factor (get the value back to )
-off	--value_offset	default=0.0, type=float, 	Value offset from zero
-vds	--value_dist	default=0.0, type=float, 	Value disturbance factor






'''
from random import *

from matplotlib.pyplot import xcorr
x=0


Partition = {
	"Value": {
		"Current": 0, 				# Currently calculated Value
		"Previous": 0,				# Previously Calculated Value
		"PointInTime": 1			# Point in Time of current calculated Value (1 day * 24 h * 60 min * 60 sec + 1000 ms = 86.400.000)
	}
	"Oscilator": {
		"Period": 1, 				# 0-inf milliseconds
		"Amplitude": 1				# 0-inf
	}
	"Randomizer": {
		"Gain": 1,					# 0-inf
		"Pull": 0.01				# 0-1
	}
	"Filter": {
		"Alpa": 0.5,					# 0-1
		"Min": 0.0,					# 0-inf
		"Max": 0.0					# 0-inf
	}
}

p1 = Partition
p1["Oscilator"]["Period"] = 3000
p1["Oscilator"]["Amplitude"] = 1
p1["Randomizer"]["Gain"] = 1
p1["Randomizer"]["Pull"] = 0.01
p1["Filter"]["Alpa"] = 0.5

p2 = p1
p2["Oscilator"]["Period"] = 37000
p2["Oscilator"]["Amplitude"] = 2
p2["Randomizer"]["Gain"] = 1
p2["Randomizer"]["Pull"] = 0.01
p2["Filter"]["Alpa"] = 0.5

p3 = p2
p3["Oscilator"]["Period"] = 413000
p3["Oscilator"]["Amplitude"] = 3
p3["Randomizer"]["Gain"] = 1
p3["Randomizer"]["Pull"] = 0.01
p3["Filter"]["Alpa"] = 0.5

def worker():
	
	for i in range(1000000):
		p1 = partition_calc(p1)
		p2 = partition_calc(p2)
		p3 = partition_calc(p3)
		v = p1 + p2 + p3



def partition_calc(partition):



def ValueSim(val,vcr=1.0,fis=0.01,fcr=0.1,vnf=0.9999,off=0.0,vds=0.0,):
	global x
	x = Filter(fcr*(random()-0.5),x,fis)
	return vnf*(Filter(vcr*(random()-0.5),val,fis+x))+vds+off

def Filter(val, val_old, alpha,):
 	return val * (1.0 - alpha) + (val_old * alpha)

