/*
  STA.cpp - Woermann Automation
  Statistics Processing Class
  Created 2020-01-08.
  
  Info:
  Call the constructor to build an instance of this class.
  Call the Instance.Update procedure to update the values (cyclic update)
  Call the Instance.Init to Initialize the Value and Statistics 

  ToDo:
  #Tha Statistics are calculated from the raw value, should be from filtered value?
	
*/

#include "STA.h"

// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up Statistics Module
 * 
 *  @return  none
 */
STA::STA() {

	Init();
}

// STA Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update STA
 *  @param 	_Val
 *			Value to Process (Float)
 *  @return  none
 */
void STA::Update(float _Val) {
	// Statistics
	if (Ini) {
		Min = _Val;
		Max = _Val;
		Ini = false;
	}
	if (_Val > Max) {
		Max = _Val;
	}
	else if (_Val < Min) {
		Min = _Val;
	}
	Avg = (Avg * float(AvgCnt) + _Val) / float(AvgCnt ++);
}
// Init Filter ------------------------------------------------------------------------------------
/*!
 *  @brief	Initialize Statistics
 *  @param 	_Val
 *			Value to Process (Float)
 *  @return  none
 */
void STA::Init() {
	Val = 0;
	Min = 0;
	Max = 0;
	Avg = 0;
	AvgCnt = 0;
	Ini = true;
}

