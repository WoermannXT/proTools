/*
  SEQ.cpp - Woermann Automation
  Sequence Processing Class
  Created 2020-04-12
  
  ToDo:
*/

#include "SEQ.h"

// Constructor--------------------------------------------------------------------------------------
// StepMap[16] = Step Number to Step ID Map
// SStNoMax = Highest Step Number used, after this jump back to Step 0
/*!
 *  @brief	Set up the Filter Module
 *  @param 	_StepMap[16]
 *			Step Number to Step ID Map, maximum of 16 steps can be defined, if any step other than Step0 (SStNoNext) is configured with StepID 0 the sequence is reset and idle (char)
 *  @return  none
 */
SEQ::SEQ(char _StepMap[16]) {
	StepMap = _StepMap;		// Only 16 Steps are available (0-15)
	Init();
}
// SEQ Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update the Filter Module
 * 
 *  @return SEQ.SStID: Current StepID (char)
 */
char SEQ::Update() {
	// Pre Step Controls ------------------------------------------------------
	if (SStA){		// Change to next step
		//SStID = StepMap[SStNo];		// Write current Step ID
		SStFC = false;					// Reset First Cycle Flag
		if (SSt0) Ini = false;
	}
	else {	
		SStNo = SStNoNext;				// Load Next STep Number (can be defined by user program)
		SStID = StepMap[SStNo];			// Set current Step ID
		SStFC = true;					// Set First Cycle Flag
		SSt0 = SStNo == 0;				// Define Step 0 Flag
		// Check End (StepID = 0) and write next Step Number
	}

	// Post Step Controls -----------------------------------------------------
	if (SStD){
		SStA = false;
		SStD = false;
	}
	else {
		SStA = true;
	}
	// Define next Step Nomber and get Next Step ID
	if (StepMap[SStNoNext] == 0) {
		SStNoNext = 0;
		SStIDNext = 0;
	}	
	else {
		SStNoNext = SStNo + 1;
		SStIDNext = StepMap[SStNoNext];
	}

	// Return the current running Step ID -------------------------------------
	return SStID;
}

// Initialise -------------------------------------------------------------------------------------
// 
/*!
 *  @brief	Initialize the SEQ Module; Set Step Done Flag and Define Step 0 as next Step
 * 
 *  @return none
 */
void SEQ::Init() {
	SStNoNext = 0;
	SStD = true;
	Ini = true;
}