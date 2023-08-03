/*
  MIX.cpp - Woermann Automation Library.
  Created 2019-12-20.

	Mix Quad X
    1CW   2CC
       \ /
        ^
       / \
    4CC   3CW

	Mix Quad +
       	1CW
    	 |
	4CC--^--2CC
    	 |
    	3CW   

	Mix V-Tail
    1LER  2RER
	  \   /
       \ /
        ^  

  ToDo:
	Channel Maximum Correction
		Limit to Maximum and
		Compenste exess to other channels???
*/


#include "MIX.h"

// Constructor--------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the Mixer Module
 *  @param 	_ChMax
 *			Channel Maximum Value (int)
 *  @param 	_ChMin
 *			Channel Minimum Value (int)
 *  @param 	_PGain
 *			Pitch Gain (float)
 *  @param 	_RGain
 *			Roll Gain (float)
 *  @param 	_YGain
 *			Yaw Gain (float)
 *  @param 	_TGain
 *			Throttle Gain (float)
 *  @return  none
 */	
MIX::MIX(int _ChMax, int _ChMin, float _PGain, float _RGain, float _YGain, float _TGain) {
	ChMax = _ChMax;
	ChMin = _ChMin;

	PGain = _PGain;
	RGain = _RGain;
	YGain = _YGain;
	TGain = _TGain;
	
}
// MIX Algorithm -----------------------------------------------------------------------------------
/*!
 *  @brief	Update Quad X Config of the Mixer Module
 *  @param 	_Pitch
 *			Pith Setpoint (nose up = negative) (float)
 *  @param 	_Roll
 *			Roll Setpoint (left = negative) (float)
 *  @param 	_Yaw
 *			Yaw Setpoint (CCW = negative) (float)
 *  @param 	_Throttle
 *			Throttle Setpoint (direct; less = negative) (float)
 *  @return  none
 */
void MIX::UpdateQX(float _Pitch, float _Roll, float _Yaw,  float _Throttle,) {

	// Compensate Gains
	Pitch = _Pitch * PGain;
	Roll = _Roll * RGain;
	Yaw = _Yaw * YGain;
	Throttle = _Throttle * TGain;

	// Calculate Outputs
	Out.S1 = int( Throttle - Pitch - Roll + Yaw );		// front left CW
	Out.S2 = int( Throttle - Pitch + Roll - Yaw );		// front right CCW
	Out.S3 = int( Throttle + Pitch + Roll + Yaw );		// rear right CW
	Out.S4 = int( Throttle + Pitch - Roll - Yaw );		// rear left CCW
}

/*!
 *  @brief	Update Quad Plus Config of the Mixer Module
 *  @param 	_Pitch
 *			Pith Setpoint (nose up = negative) (float)
 *  @param 	_Roll
 *			Roll Setpoint (left = negative) (float)
 *  @param 	_Yaw
 *			Yaw Setpoint (CCW = negative) (float)
 *  @param 	_Throttle
 *			Throttle Setpoint (direct; less = negative) (float)
 *  @return  none
 */
void MIX::UpdateQP(float _Pitch, float _Roll, float _Yaw,  float _Throttle,){

	// Compensate Gains
	Pitch = _Pitch * PGain;
	Roll = _Roll * RGain;
	Yaw = _Yaw * YGain;
	Throttle = _Throttle * TGain;

	// Calculate Outputs
	Out.S1 = int( Throttle - Pitch        + Yaw );		// front CW
	Out.S2 = int( Throttle         + Roll - Yaw );		// right CCW
	Out.S3 = int( Throttle         + Roll + Yaw );		// rear CW
	Out.S4 = int( Throttle + Pitch        - Yaw );		// left CCW

}

/*!
 *  @brief	Update V-Tail Config of the Mixer Module
 *  @param 	_Pitch
 *			Pith Setpoint (nose up = negative) (float)
 *  @param 	_Roll
 *			Roll Setpoint (left = negative) (float)
 *  @param 	_Yaw
 *			Yaw Setpoint (CCW = negative) (float)
 *  @param 	_Throttle
 *			Throttle Setpoint (direct; less = negative) (float)
 *  @return  none
 */
void MIX::UpdateVT(float _Pitch, float _Roll, float _Yaw,  float _Throttle,){

	// Compensate Gains
	Pitch = _Pitch * PGain;
	Roll = _Roll * RGain;
	Yaw = _Yaw * YGain;
	Throttle = _Throttle * TGain;
	
	// Calculate Outputs
	Out.S1 = int( Roll + Yaw - Throttle - Pitch);		// Left Elerudder
	Out.S2 = int( Roll + Yaw + Throttle + Pitch);		// Right Elerudder

}
// Initialise -------------------------------------------------------------------------------------
/*!
 *  @brief	Initialize the MIX Module:
 * 			Set all Outputs to 0
 *  @return none
 */
void MIX::Init() {
	Out.S1 = 0;
	Out.S2 = 0;
	Out.S3 = 0;
	Out.S4 = 0;
}