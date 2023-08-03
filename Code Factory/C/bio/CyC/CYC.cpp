/*
  CYC - Woermann Automation
  CYC Processing Class
  Created 2021-04-19

  Info:

  ToDo:
	
*/

#include "CYC.h"

// Constructor-------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the CYC Module
 * 
 *  @return  none
 */
CYC::CYC() {
	Init();
}
// CYC Algorithm ----------------------------------------------------------------------------------
/*!
 *  @brief	Update the CYC Module, this should be done at an interval rate of the defined time base in the constructor
 *  @param 	_SysT
 *			System Time im microseconds
 *  @return none
 */
void CYC::Update(unsigned long _SysT) {
	// CYC Initialize ---------------------------------------------------------
	if (Ini) { 
		Ini = false;

		CycT = 0;
		iCycC = 0;
		CycC = 0;
		CycPS = 1;
		SysT = _SysT;

		cm.m10ms = 0;
		cm.m100ms = 0;
		cm.m1s = 0;
		cm.m6s = 0;
		cm.m10s = 0;
		
		ti.ms = 0;
		ti.s = 0;
		ti.m = 0;
		ti.h = 0;
		ti.d = 0;

		return;
	}

	// CYC Algorithm ----------------------------------------------------------
	// --- Cycle Time Measurement
	if (_SysT >= SysT) {
		CycT = _SysT - SysT;
	}
	SysT = _SysT;
	CycC ++;

	// --- Generate Cycle Slice Flags ---------------------
	if ( iCycC > 15015 ) iCycC = 1;		// If lst run was 15016 (all cycles true, 3-13) then restart a 1
	else iCycC ++;						// else inc

	if(iCycC % 2 == 0) cs.x2e = true;
	else cs.x2e = false;
	cs.x2o = !cs.x2e;
	
	if ( iCycC %  3 == 0 )	cs.x3 = true;
	else cs.x3 = false;
	if ( iCycC %  5 == 0 ) 	cs.x5 = true;
	else cs.x5 = false;
	if ( iCycC %  7 == 0 ) 	cs.x7 = true;
	else cs.x7 = false;
	if ( iCycC % 11 == 0 )	cs.x11 = true;
	else cs.x11 = false;
	if ( iCycC % 13 == 0 )	cs.x13 = true;
	else cs.x13 = false;

	// --- Generate Clock Flags ----------------------------
	// 10 milli seconds
	cm.m10ms += CycT;
	if (cm.m10ms >= 100000) {
		cp.x10ms = true;
		ct.x10ms = !ct.x10ms;
		cm.m10ms -= 10000;
	}
	else cp.x10ms = false;
	// 100 milli seconds
	cm.m100ms += CycT;
	if (cm.m100ms >= 100000) {
		cp.x100ms = true;
		ct.x100ms = !ct.x100ms;
		cm.m100ms -= 100000;
	}
	else cp.x100ms = false;
	// 1 second
	cm.m1s += CycT;
	if (cm.m1s >= 1000000) {
		cp.x1s = true;
		ct.x1s = !ct.x1s;
		cm.m1s -= 1000000;
		CycPS = CycPSCnt;	// Save Cycles per Second
		CycPSCnt = 1;		// And Reset
	}
	else {
		cp.x1s = false;
		CycPSCnt += 1;		// Count Cycles per Second
	}
	// 6 second
	cm.m6s += CycT;
	if (cm.m6s >= 6000000) {
		cp.x6s = true;
		ct.x6s = !ct.x1s;
		cm.m6s -= 6000000;
	}
	else cp.x6s = false;
	// 10 seconds
	cm.m10s += CycT;
	if (cm.m10s >= 10000000) {
		cp.x10s = true;
		ct.x10s = !ct.x1s;
		cm.m10s -= 10000000;
	}
	else cp.x10s = false;		
	// 60 seconds
	cm.m60s += CycT;
	if (cm.m60s >= 60000000) {
		cp.x60s = true;
		ct.x60s = !ct.x1s;
		cm.m60s -= 60000000;
	}
	else cp.x60s = false;		
	// 100 seconds
	cm.m100s += CycT;
	if (cm.m100s >= 100000000) {
		cp.x100s = true;
		ct.x100s = !ct.x1s;
		cm.m100s -= 100000000;
	}
	else cp.x100s = false;		

// --- Time ----------------------------
	ti.ms = cm.m1s / 1000;
	if (cp.x1s) {
		ti.s ++;
		if (ti.s >= 60) {
			ti.s = 0;
			ti.m ++;
			if (ti.m >= 60) {
				ti.m = 0;
				ti.h ++;
				if (ti.h >= 24) {
					ti.h = 0;
					ti.d ++;
				}
			}
		}
	}


} // End CYC

// Initialise -------------------------------------------------------------------------------------
/*!
 *  @brief	Initialize CYC Variables
 *  @param 	_SysT
 *			System Time im micros
 *  @return none
 */
void CYC::Init() {
	CycT = 0;
	iCycC = 0;
	CycC = 1;
	CycPS = 1;
	SysT = 0;

	cm.m10ms = 0;
	cm.m100ms = 0;
	cm.m1s = 0;
	cm.m6s = 0;
	cm.m10s = 0;
	
	ti.ms = 0;
	ti.s = 0;
	ti.m = 0;
	ti.h = 0;
	ti.d = 0;

	Ini = true;
}

// Set Time ---------------------------------------------------------------------------------------
/*!
 *  @brief	Set Time to Preset
 *  @param 	_sSet
 *			Setpoint for Seconds
 *  @param 	_mSet
 *			Setpoint for Minutes
 *  @param 	_hSet
 *			Setpoint for Hours
 *  @param 	_dSet
 *			Setpoint for Days
 *  @return none
 */
void CYC::SetTime( unsigned long _sSet, unsigned long _mSet, unsigned long _hSet, unsigned long _dSet) {
		ti.s = _sSet;
		ti.m = _mSet;
		ti.h = _hSet;
		ti.d = _dSet;
}
