/*
  SET.cpp - Woermann Automation
  Setpoint Processing Class
  Created 2019-12-03
  
  ToDo:
	
*/

#include "SET.h"

// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up Setpoint / Value Processing
 *  @param 	_Set
 *			Desired Setpoint
 *  @param 	_LLV
 *			Low Low Value Setpoint
 *  @param 	_LV
 *			Low Value Setpoint
 *  @param 	_HV
 *			High Value Setpoint
 *  @param 	_HHV
 *			High High Value Setpoint
 *  @return  none
 */
SET::SET(float _Set, float _LLV, float _LV, float _HV, float _HHV){
	Set = _Set;
	LLV = _LLV;
	LV = _LV;
	HV = _HV;
	HHV = _HHV;
	Init( 0.0f ): 
}
// SET Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update SET
 *  @param 	_Val
 *			Current Value
 *  @return  SET.D Setpoint reached (Value >= Setpoint)
 */
bool SET::Update(float _Val) {
	Ini = false;
	D = _Val >= Set;	// Setpoint Reached (Val >= SP)
	LL = _Val <= LLV;	// Low Signal (Val <= LV)
	L = _Val <= LV;		// Low Signal (Val <= LV)
	H = _Val >= HV;		// High Signal (Val >= HV)
	HH = _Val >= HHV;	// High Signal (Val >= HV)
	E = Set - Val;		// Error (Set - Val)
	Val = _Val;
	return D;
}
// Initialize Setpoint ----------------------------------------------------------------------------
/*!
 *  @brief	Initialize the Setpoint Module
 *  @param 	_Val
 *			Value to Initialize to (Float)
 *  @return none
 */
void SET::Init(float _Val) {
	Ini = true;
	D = false;		// Setpoint Reached (Val >= SP)
	LL = false;		// Low Signal (Val <= LLV)
	L = false;		// Low Signal (Val <= LV)
	H = false;		// High Signal (Val >= HV)
	HH = false;		// High Signal (Val >= HHV)
	E = 0.0f;		// Error (Set -Val)
	Val = _Val;
}