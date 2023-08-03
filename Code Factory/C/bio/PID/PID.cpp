/*
  PID - Woermann Automation
  PID Processing Class
  Created 2019-12-03
  - Changed D-Part calculation from dE to delta Val (dE not needed anymore)
	this prevents big fluctuations during change of Setoint (instantanious big changes)
	during control without Setoint change, the logig is similar to dE
  - Timebase is not calculated anymore, now an input parameter
	The PID should be called with an Interrupt to have a stabel Update Time defined in Constructor
  - Chenged I-Part Calculation to be robust agaist Ki changes
  - Added the Disturbance Value method witch summs up all disturbances and adds them to teh PID 
  	Output at next calculation (Update) 

  Info:

  ToDo:
	
*/

#include "PID.h"

// Constructor-------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the PID; for Inverse control logic use negative values for _KP, _Ki and _Kd
 *  @param 	_Kp
 *			Gain for Proportional Part 
 *  @param 	_Ki
 *			Gain for Integral Part 
 *  @param 	_Kd
 *			Gain for Derivative  Part 
 *  @param 	_OMin
 *			Minimum Output (must be smaller than OMax)
 *  @param 	_OMax
 *			Maximum Output (must be larger than OMin)
 *  @param 	_OIni
 *			Initial Output Value (if COn is false or Ini is true)
 *  @param 	_TBase
 *			PID Update Time in Seconds (eg. 0.01), defines what is the time between updates
 *  @param 	_Inv
 *			Inverted control logic eg. cooler, higher output results in lower values (bool) 
 *  @return  none
 */
PID::PID(float _Kp, float _Ki, float _Kd, float _OMin, float _OMax, float _OIni, float _TBase, bool _Inv) {
	TBase = _TBase;	
	Kp = _Kp;
	Ki = _Ki * TBase;
	Kd = _Kd / TBase;
	if (_OMin > _OMax) {
		OMax = _OMin;
		OMin = _OMax;
	}
	else {
		OMin = _OMin;
		OMax = _OMax;
	} 
	OIni = _OIni;
	Inv = _Inv;
	Init(OIni);
}
// PID Algorithm ----------------------------------------------------------------------------------
/*!
 *  @brief	Update the PID, this should be done at an interval rate of the defined time base in the constructor
 *  @param 	_Set
 *			Setoint (tis is the required / desired value)
 *  @param 	_Val
 *			Process Value (this is the currently measured value)
 *  @param 	_On
 *			Control On (PID Algorithm actice, if not On then initialise value to OInit
 *  @return Output Value (Out)
 */
float PID::Update(float _Set, float _Val, bool _On) {
	// PID Initialize ---------------------------------------------------------
	if (Ini) { 
		dPV = E = 0;
		Out = OIni;
	}
	// PID Algorithm ----------------------------------------------------------
	else { 	
		dPV = Val - _Val;
		E = _Set - _Val;
		sPID = Kp * (E1 - E) + Ki * E + Kd * (dPV1 - dPV) + PSV;		
		if (Inv) Out -= sPID;
		else Out += sPID;
		if (Out > OMax) Out = OMax;
		else if (Out < OMin) Out = OMin;
	}
	// PID Finalise  ----------------------------------------------------------
	Ini = !_On;
	E1 = E;
	dPV1 = dPV;
	Val = _Val;
	PSV = 0;
	return Out;
}
/*!
 *  @brief	Update the PID, this should be done at an interval rate of the defined time base in the constructor
 *  @param 	_Set
 *			Setoint (tis is the required / desired value)
 *  @param 	_Val
 *			Process Value (this is the currently measured value)
 *  @param 	_On
 *			Control On (PID Algorithm actice, if not On then initialise value to OInit
 *  @return Output Value (Out)
 */
float PID::UpdatePI(float _Set, float _Val, bool _On) {
	// PID Initialize ---------------------------------------------------------
	if (Ini) { 
		E = 0;
		Out = OIni;
	}
	// PID Algorithm ----------------------------------------------------------
	else { 	
		E = _Set - _Val;
		sPID = Kp * (E1 - E) + Ki * E + PSV;					
		if (Inv) Out -= sPID;
		else Out += sPID;
		if (Out > OMax) Out = OMax;
		else if (Out < OMin) Out = OMin;
	}
	// PID Finalise  ----------------------------------------------------------
	Ini = !_On;
	E1 = E;
	Val = _Val;
	PSV = 0;
	return Out;
}
/*!
 *  @brief	Update the PID, this should be done at an interval rate of the defined time base in the constructor
 *  @param 	_Set
 *			Setoint (tis is the required / desired value)
 *  @param 	_Val
 *			Process Value (this is the currently measured value)
 *  @param 	_On
 *			Control On (PID Algorithm actice, if not On then initialise value to OInit
 *  @return Output Value (Out)
 */
float PID::UpdateP(float _Set, float _Val, bool _On) {
	// PID Initialize ---------------------------------------------------------
	if (Ini) { 
		E = 0;
		Out = OIni;
	}
	// PID Algorithm ----------------------------------------------------------
	else { 	
		E = _Set - _Val;
		sPID = Kp * (E1 - E) + PSV;			
		if (Inv) Out -= sPID;
		else Out += sPID;
		if (Out > OMax) Out = OMax;
		else if (Out < OMin) Out = OMin;
	}
	// PID Finalise  ----------------------------------------------------------
	Ini = !_On;
	E1 = E;
	Val = _Val;
	PSV = 0;
	return Out;
}
/*!
 *  @brief	Speed Optimized Update the PI, this should be done at an interval rate of the defined time base in the constructor

 *  @param 	_Set
 *			Setoint (tis is the required / desired value)
 *  @param 	_Val
 *			Process Value (this is the currently measured value)
 *  @return Output Value (Out)
 */
float PID::UpdateSO(float _Set, float _Val, bool _On) {
	// PID Algorithm ----------------------------------------------------------
	E = _Set - _Val;
	Out += Kp * (E1 - E) + Ki * E;
	
	// PID Finalise  ----------------------------------------------------------
	E1 = E;
	Val = _Val;
	return Out;
}
// Initialise -------------------------------------------------------------------------------------
/*!
 *  @brief	Initialize the PID to OIni
 *  @param 	_OIni
 *			Initial Output Value (if COn is false)
 *  @return none
 */
void PID::Init(float _OIni) {
	Ini = true;
	OIni = _OIni;
	Out = _OIni;
	PSV = 0;
}

// Set/Update P Value Factor ----------------------------------------------------------------------
/*!
 *  @brief	Adjust Proportional Gain
 *  @param 	_Kp
 *			Adjust Factor for Proportional Part Gain
 *  @return none
 */
void PID::SetKp(float _Kp) {
	Kp = _Kp;
}

// Set/Update I Value Factor ----------------------------------------------------------------------
/*!
 *  @brief	Adjust Integral Gain with Time Base Correction
 *  @param 	_Ki
 *			Value for Integral Part Gain
 *  @return none
 */
void PID::SetKi(float _Ki) {
	Ki = _Ki * TBase;
}

// Set/Update D Value Factor ---------------------------------------------------------------------
/*!
 *  @brief	Adjust Differential Gain with Time Base Correction
 *  @param 	_Kd
 *			Value for Differential Part Gain
 *  @return none
 */
void PID::SetKd(float _Kd) {
	Kd = _Kd / TBase;
}

// Adjust Output by a Pre-Sense Value (any infuential or disturbance value) ----------------------
/*!
 *  @brief	Adjust the PID Output by one or more pre-sense value that typically disturbes the value (_Val) and that 
 *			can be given to the PID to act before a measurement update. Important to know that the _PSV is compleatly 
 *			compensated for, so the PID output will be changed by the PSV every time it is updated.
 *			Not used for "UpdateSO"
 *  @param 	_PSV
 *			Pre-Sense Value to be added to the output of the PID
 *  @param 	_Fact
 *			Factor to adjust the magnitude and direcion of the disturbance
 *  @return none
 */
void PID::PreSense(float _PSV, float _Fact) {
	PSV += (_PSV * _Fact);
}
