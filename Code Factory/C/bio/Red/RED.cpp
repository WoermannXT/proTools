/*
  RED.cpp - Woermann Automation.
  Created 2019-12-03.
  
  ToDo:
	
*/

#include "RED.h"

// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the Value Redundancy Module
 *  @param 	_DeltaMax
 *			Maximum acceptable delta between the two values before one is discarded as false reading
 *  @return  none
 */
RED::RED(float _DeltaMax) {
	DeltaMax = _DeltaMax;
	Init(0.0f);
}
// RED Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	RED Algorithm to return the most plausible value of a value pair 
 *  @param 	_Raw1
 *			Value 1 for redundancy calculation
 *  @param 	_Raw2
 *			Value 2 for redundancy calculation
 *  @return Calculated Redundant Value
 */
float RED::Update(float _Raw1, float _Raw2) {
	// Define High and Low ----------------------------------------------------
	if (_Raw2 > _Raw1) {
		High = _Raw2;
		Low = _Raw1;
	}
	else {
		High = _Raw1;
		Low = _Raw2;
	}
	// Define Delta and Value -------------------------------------------------
	Delta = High - Low;
	if (Delta < DeltaMax) { 	// Delta not too large
		Ini = false;			// Redundancy Pair Calculation OK, reset Ini
		dMax = false;
		if (Val > High) {		// Value bigger than High
			Val = High;
		}
		else if  (Val < Low) {	// Value smaller than Low
			Val = Low;
		}
		else {
			Val = (High + Low) / 2.0f;
		}
	}
	else {						// Delta is too large
		if (Val > (High + Low) / 2.0f) {
			Val = High;
		}
		else {
			Val = Low;
		}
		dMax = true;
	}
	return Val;
}
// Initialise -------------------------------------------------------------------------------------
/*!
 *  @brief	Initialize the RED Module
 *  @param 	_Val
 *			Initialization Value
 *  @return none
 */
void RED::Init(float _Val) {
	Ini = true;
	Val = _Val;
}


