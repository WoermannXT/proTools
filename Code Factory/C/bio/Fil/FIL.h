/*
  VAL.h - Woermann Automation Library.
  Created by EWo, 2020-01-08.
*/

#ifndef FIL_h
#define FIL_h

class FIL {
  // Class Member Variables
  public:
	FIL(float _dMin, float _dMax, float _Alpha);
    float dMin;				// Delta Minimum (Hysteresis for Update if Outside - Deadband)
    float dMax;				// Delta Maximum (Hysteresis for Update if Inside - Limiting Change)
	float Alpha;			// Factor for Filter
 
	float Update(float _Raw);
	float Raw;				// Raw Value
	float Val;				// Filterde Value
	
	void Init(float _Raw);
	bool Ini;				// Initialize Module

	private:
	float Delta;			// Delta (Change) of Value
   };
#endif

