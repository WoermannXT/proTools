/*
  CNT - Woermann Automation
  Counter Processing Class
  Created 2020-04-12
  
  ToDo:
	Count by Value needs to be added and tested

*/

#include "CNT.h"

// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the Counter Module
 *  @param 	_Fact
 *			Factor for Counter Value to Process Value; value per counter impulse (float)
 *  @param 	_Type
 *			Actuator Type (uint8_t):
 *			0 = Count with Positive Pulse,
 *			1 = Count with Negative Pulse,	
 *			2 = Count when True,
 *			3 = Count when False,
 *			4 = ....
 *			10 = Count up with Raw Value Positive Delta (+/+),
 *			11 = Count up with Raw Value Negative Delta (-/+),	
 *			12 = Count up with Raw Value any Delta (+/+, -/+),
 *			13 = Count sync with Raw Value Delta (+/+, -/-),
 *			14 = Count sync with Raw Value any Delta (+/+, -/-),
 *			15 = ....
 *  @return  none
 */
CNT::CNT(float _Fact, uint8_t _Type) {
	Fact = _Fact;
	Type = _Type;
	Init();
}

// CNT Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update the Counter Module
 *  @param 	_Raw
 *			Raw Signal to Process (bool)
 *  @param 	_Down
 *			Count Down (bool)
 *  @return CNT.Val: Counter Process Value (float)
 */
float CNT::Update(bool _Raw, bool _Down) {
	switch ( Type ) {
		case 0:			// Count when Positive Edge
			if (_Raw && !Raw) {
				Ini = false;
				if(_Down) {
					Cnt --;
				}
				else {
					Cnt ++;
				}
			}
		break;
		case 1:			// Count when Negative Edge
			if (!_Raw && Raw) {
				Ini = false;
				if(_Down) {
					Cnt --;
				}
				else {
					Cnt ++;
				}
			}
		break;
		case 2:			// Count when True
			if (_Raw) {
				Ini = false;
				if(_Down) {
					Cnt --;
				}
				else {
					Cnt ++;
				}
			}
		break;
		case 3:			// Count when False
			if (!_Raw) {
				Ini = false;
				if(_Down) {
					Cnt --;
				}
				else {
					Cnt ++;
				}
			}
		break;
	}
	Raw = _Raw;
	Val = Fact * Cnt;
	return Val;
}

/*!
 *  @brief	Update the Counter Module by Value
 *  @param 	_RawVal
 *			Raw Signal to Process (float)
 *  @param 	_Down
 *			Count Down (bool)
 *  @return CNT.Val: Counter Process Value (float)
 */
float CNT::UpdateByVal(float _RawVal, bool _Down) {
	if (Ini) {
		RawVal = _RawVal;
	}
	else {
		Ini = false;
		RawD = _RawVal - RawVal;
		switch ( Type ) {
			case 10:			// Count up with Raw Value Positive Delta (+/+)
				if (RawD >> 31) {
					RawVal = _RawVal;
				}
				else {
					Val += Fact * RawD;
				}
			break;
			case 11:			// Count up with Raw Value Negative Delta (-/+)
				if (RawD >> 31) {
					Val -= Fact * RawD;
				}
				else {
					RawVal = _RawVal;
				}
			break;
			case 12:			// Count up with Raw Value any Delta (+/+, -/+)
				Val += Fact * fabs(RawD);
			break;
	1	}
	}

	RawVal = _RawVal;
	return Val;
}

// Reset the Counter to Zero 
/*!
 *  @brief	Initialize the Counter Module
 *  @return none
 */
void CNT::Init() {
	Ini = true;
	Cnt = 0;
	Val = 0.0f;
}


