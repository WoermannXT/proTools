
'''
Value Simulator

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

def ValueSim(val,vcr=1.0,fis=0.01,fcr=0.1,vnf=0.9999,off=0.0,vds=0.0,):
	global x
	x = Filter(fcr*(random()-0.5),x,fis)
	return vnf*(Filter(vcr*(random()-0.5),val,fis+x))+vds+off

def Filter(val, val_old, alpha,):
 	return val * alpha + (val_old * (1.0 - alpha))

