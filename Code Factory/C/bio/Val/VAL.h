/*
  VAL - Woermann Automation
  Value Processing Class
  Created 2019-12-03
*/	
#ifndef VAL_h
#define VAL_h

class VAL { 
	// Class Member Variables
	public:
		VAL(float _RawMin, float _RawMax, float _ValMin, float _ValMax, char _Type);
		float RawMin;			// Raw Value Minimum (Scale)
		float RawMax;			// Raw Value Maximum (Scale)
		float ValMin;			// Value Minimum (Scale)
		float ValMax;			// Value Maximum (Scale)
		char Type;				// Value Type, 0 = Raw; 1 = ReScale; 2 = Calibrate; 3 = ReScale and Calibrate

		float Fact;				// Factor for Value Calibration
		float Offs;				// Offset for Value Calibration

		float Update(float _Raw);
		float Val;				// Processed Value

		void Init();
		bool Ini;				// Initialize Module
		
		void Tara();			// Set Tara of the Value with current Value
		

};
#endif
