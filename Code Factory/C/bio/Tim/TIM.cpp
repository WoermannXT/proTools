/*
  TIM - Woermann Automation
  Timer Processing Class
  Created 2021-04-12
  
  Info:

  ToDo:

*/

#include "TIM.h"

// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the Timer Module
 *  @param 	_Set
 *			Timer Setpoint (float)
 *  @param 	_Type
 *			Timer Type (byte):
 *			0 = Microsecond Timer,
 *			1 = Millisecond Timer,	
 *			2 = Second Timer,
 *			3 = Minute Timer,
 *			4 = Hour Timer,
 *			5 = ....
 *  @return  none
 */
TIM::TIM(float _Set, char _Type) {
	Set = _Set;
	Type = _Type;
	Init();
}

// TIM Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update the Timer Module
 *  @param 	_CycT
 *			Previous Cycle Time in Microseconds (unsigned long)
 *  @return  TIM.D Timer Done (Setpoint reached)
 */
bool TIM::Update(unsigned long _CycT) {
	Ini = false;
	// Claculate Timer --------------------------------------------------------
    // Start Time Counter if "Start"
	if (S & !R) {
		if (!P) {		// Only Count if not "Pause"
			Tim += _CycT;
		}
		else {
			P = false;
		}		
	}
	else {			// Reset of not "Start"
		Tim = 0;
		R = false;
	}
	// Calculate Timer Value --------------------------------------------------
	switch ( Type ) {
		case 0:			// Microsecond Timer
			Val = float(Tim);
		break;		
		case 1:			// Millisecond Timer
			Val = float(Tim) / 1000.0f;
		break;
		case 2:			// Second Timer
			Val = float(Tim) / 1000000.0f;
		break;
		case 3:			// Minute Timer
			Val = float(Tim) / 60000000.0f;
		break;
		case 4:			// Hour Timer
			Val = float(Tim) / 3600000000.0f;
		break;
	}
	D = Val >= Set;
	return D;
}

// Reset the Timer to Zero 
/*!
 *  @brief	Initialize Timer
 * 
 *  @return  none
 */
void TIM::Init() {
	Tim = 0;
	Val = 0.0f;
	S = false;
	P = false;
	D = false;
	Ini = true;
}


