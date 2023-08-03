/*
  FIL.cpp - Woermann Automation Library.
  Created by EWo, 2020-01-08.
  
  Info:
  Call the constructor to build an instance of this class.
  Call the Instance.Update procedure to update the values (cyclic update)
  Call the Instance.Init to Initialize the Value and Statistics 

  ToDo:

	
*/

#include "Arduino.h"

#include "FIL.h"


// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the Filter Module
 *  @param 	_dMin
 *			Delta Minimum (If Delta < dMin then no update of Filtered Value) (float)
 *  @param 	_dMax
 *			Delta Maximum (If Delta > dMax then Max / Min is used to update Filtered Value) (float)
 *  @param 	_Alpha
 *			Factor for Filter 0.0 (0% = no filter) to 1.0 (100% = freeze) (float)
 *  @return  none
 */
FIL::FIL(float _dMin, float _dMax, float _Alpha) {
	dMin = _dMin;
	dMax = _dMax;
	Alpha = _Alpha;
}

// FIL Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update the Filter Module
 *  @param 	_Raw
 *			Value to Process (Float)
 *  @return FIL.Val: Filtered Value (float)
 */
float FIL::Update(float _Raw) {
	Ini = false;
	Delta = Raw - _Raw;
	// Check if Minimum Change 
	if (abs(Delta) < dMin) {
		Raw = _Raw;
		return Val;
	}
	// Check if Maximum Cahnge Positive
	else if (Delta > dMax) {
		Raw = _Raw + dMax;
	}
	// Check if Maximum Cahnge Negative
	else if (-Delta > dMax) {
		Raw = _Raw - dMax;
	}
	// Else just use Raw Value
	else {
		Raw = _Raw;
	}
	Val = Raw * (1.0 - Alpha) + (Val * Alpha);
	// Return Filtered Value
	return Val;
}
// Initialize Filter ------------------------------------------------------------------------------
/*!
 *  @brief	Initialize the Counter Module
 *  @param 	_Raw
 *			Value to Initialize to (Float)
 *  @return none
 */
void FIL::Init(float _Raw) {
	Ini = true;
	Raw = _Raw;
	Val = Raw;
}

