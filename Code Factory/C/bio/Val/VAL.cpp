/*
  VAL - Woermann Automation
  Value Processing Class
  Created 2019-12-03
  
  ToDo:
	
*/

#include "VAL.h"

// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the Value Module
 *  @param 	_RawMin
 *			Raw Value Minimum Scale (float)
 *  @param 	_RawMax
 *			Raw Value Maximum Scale (float)
 *  @param 	_ValMin
 *			Value Minimum Scale (float)
 *  @param 	_ValMax
 *			Value Maximum Scale (float)
 *  @param 	_Type
 *			Value Type (uint8_t):
 *			0 = Raw (no rescaling, scale settings are not used),
 *			1 = Scale to ValMin / ValMax,	
 *			2 = Calibrate (+Offs*Fact),
 *			3 = Scale and Calibrate,
 *			4 = ....
 *  @return  none
 */
VAL::VAL(float _RawMin, float _RawMax, float _ValMin, float _ValMax, char _Type) {
	RawMin = _RawMin;
	RawMax = _RawMax;
	ValMin = _ValMin;
	ValMax = _ValMax;
	Type = _Type;
	Init();
}

// VAL Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update the Value Module
 *  @param 	_Raw
 *			Raw Value to Process (Float)
 *  @return  Val (float)
 */
float VAL::Update(float _Raw) {
	switch ( Type ) {
		case 0:			// Raw Value
			Val = _Raw;
		break;
		case 1:			// Scaled Value
			Val = (_Raw -  RawMin) / (RawMax - RawMin) * (ValMax - ValMin) + ValMin ;
		break;
		case 2:			// Calibrated Value
			Val = _Raw;
			Val += Offs;
			Val *= Fact;
		break;
		case 3:			// Scaled and Calibrated Value
			Val = (_Raw -  RawMin) / (RawMax - RawMin) * (ValMax - ValMin) + ValMin ;
			Val += Offs;
			Val *= Fact;
		break;
	}
	Ini = false;
	return Val;
}

// Initialis the Value
/*!
 *  @brief	Initialize the Value Module
 *  @return  none
 */
void VAL::Init() {
	Fact = 1.0f;
	Offs = 0.0f;
	Ini = true;
}

// Tara the Value to Zero by subtracting the Value from the Offset
/*!
 *  @brief	Set Tara of the Value Module
 *  @return  none
 */
void VAL::Tara() {
	Offs -= Val;
}
