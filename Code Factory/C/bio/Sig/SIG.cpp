/*
  SIG.cpp - Woermann Automation
  Signal Processing Class
  Created 2019-12-03
  
  ToDo:
	If millis() rewind then calculation TOn and TOff not correct
*/

#include "SIG.h"

// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the Signal Module
 *  @param 	_TOnSet
 *			Time Setpoint in Milliseconds to switch Signal ON (unsigned int)
 *  @param 	_TOffSet
 *			Time Setpoint in Milliseconds to switch Signal OFF (unsigned int)
 *  @param 	_Inv
 *			Inverted / Negated Raw Signal (bool)
 *  @return  none
 */
SIG::SIG(unsigned long _TOnSet, unsigned long _TOffSet, bool _Inv) {
	TOnSet = _TOnSet * 1000;		// Convert Millis to Micros
	TOffSet = _TOffSet * 1000;		// Convert Millis to Micros
	Inv = _Inv;   
	Init();
}
// SIG Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update the Signal Module
 *  @param 	_Raw
 *			Raw Signal to Process (bool)
 *  @param 	_CycT
 *			Previous Cycle Time (unsigned long)
 *  @return SIG.Sig (bool)
 */
bool SIG::Update(bool _Raw, unsigned long _CycT) {
	if (Inv) Raw = !_Raw;
	else Raw = _Raw;
	if (!Sig & Raw) { 			// Turn Off
		if (TOVal >= TOffSet) {
			Sig=true;
			negP=true;
		} 
		else TOVal += _CycT;  
	}
	else if (Sig & !Raw) {  	// Turn On
		if (TOVal >= TOnSet) {
			Sig = false;
			posP = true;
		}
		else TOVal += _CycT;  
	}
	else {						// Keep State
		negP = false;
		posP = false;
		TOVal = 0;  
	}
	return Sig;
}
// Initialise -------------------------------------------------------------------------------------
/*!
 *  @brief	Initialize the SIG Module
 *  @return none
 */
void SIG::Init() {
	Ini = true;
	Raw = false;
	if (Inv) Sig = !Raw;
	else Sig = Raw;
	negP = false;
	posP = false;
	TOVal = 0;
}