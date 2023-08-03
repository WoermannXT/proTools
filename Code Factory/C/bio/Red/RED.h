/*
  RED.h - Woermann Automation.
  Created 2019-12-03.
*/
#ifndef RED_h
#define RED_h

class RED { 
  // Class Member Variables
  public:
	RED(float _DeltaMax);
    float DeltaMax;			// Deviation Maximum

	float Update(float _Raw1, float _Raw2);
	float Val;				// Redundant Value
	float Low;				// Lower Value
	float High;				// Higher Value
	float Mean;				// Mean Value
	float Delta;			// Deveation
	bool dMax;				// Maximum Deviation between Values

	void Init(float _Val);
	bool Ini;				// Initialize Module

   };
#endif

