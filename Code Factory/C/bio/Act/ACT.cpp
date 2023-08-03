/*
  ACT.cpp - Woermann Automation
  Actuator Processing Class
  Created 2021-04-12
  Info:
	Changed to Cycle Time

  ToDo:
	Type Definition needs to be finished
*/

#include "ACT.h"

// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the Actuator Module
 *  @param 	_TOnSet
 *			Time Setpoint in Milliseconds to switch Actuator ON (unsigned int)
 *  @param 	_TOffSet
 *			Time Setpoint in Milliseconds to switch Actuator OFF (unsigned int)
 *  @param 	_TAlet
 *			Time Setpoint in Milliseconds to delay Alarm (unsigned int)
 *  @param 	_Type
 *			Actuator Type (uint8_t):
 *			0 = No Feedback,
 *			1 = Off Feedback,	
 *			2 = Off Feedback Only checked When Off,
 *			3 = On Feedback,
 *			4 = ....
 *  @return  none
 */
ACT::ACT(uint32_t _TOnSet, uint32_t _TOffSet, uint32_t _TAlSet, uint8_t _Type) {
	TOnSet = _TOnSet * 1000;		// Convert Millis to Micros
	TOffSet = _TOffSet * 1000;		// Convert Millis to Micros
	TAlSet = _TAlSet * 1000;		// Convert Millis to Micros
	Type = _Type;
	Init();
}
// ACT Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update the Actuator Module
 *  @param 	_CycT
 *			Previous Cycle Time in Microseconds (unsigned long)
 *  @return ACT.Out: Output control
 */
bool ACT::Update(uint32_t _CycT) {
	// Feedback Control -------------------------------------------------------
	switch ( Type ) {
		case 0:			// No Feedback
			FOn = COn;
		break;
		case 1:			// Off Feedback	
			FOn != Fba ^ Out;
		break;
		case 2:			// Off Feedback Only checked When Off
			FOn = !Fba & !Out;
		break;
		case 3:			// On Feedback
			FOn = Fba ^ Out;
		break;
		default : 		// Type not set correctly
			FOn = !COn;
	}
	// Alarm Evaluation -------------------------------------------------------
	if (FOn != COn) {
		if (TAlVal > TAlSet) {
			GAl = true;
		}   	
		TAlVal += _CycT;
	}
	else {
		GAl = false;
		TAlVal = 0;
	}
	
	// Output Control with Time Delay -----------------------------------------
	if (!COn & Out) { 		// Turn Off Delay
		if (TOVal >= TOffSet) {
			Out = COn;
			negP = true;
		}   
		else TOVal += _CycT;
	}
	else if (COn & !Out) {  // Turn On Delay
		TOVal += _CycT;
		if (TOVal >= TOnSet) {
			Out = COn;
			posP = true;
		}
		else TOVal += _CycT;
	}
	else {					// Keep State
		negP = false;
		posP = false;
		Out = COn;
		TOVal = 0;
	}
	Ini = false;
	return Out;
}
// Initialise -------------------------------------------------------------------------------------
/*!
 *  @brief	Initialize the ACT Module (for now only for standarisation purpose)
 *  @return none
 */
void ACT::Init() {
	Ini = true;
	COn = false;
	Out = false;
	FOn = false;
	GAl = false;
	negP = false;
	posP = false;
	TOVal = 0;
	TAlVal = 0;
}