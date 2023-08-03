/*
  SET.h - Woermann Automation
  Setpoint Processing Class
  Created 2019-12-03
*/
#ifndef SET_h
#define SET_h

class SET { 
	// Class Member Variables
	public:
		SET(float _Set, float _LLV, float _LV, float _HV, float _HHV);
		float Set;				// Setpoint
		float LLV;				// Low Low Value
		float LV;				// Low Value
		float HV;				// High Value
		float HHV;				// High High Value

		bool Update(float _Val);
		float Val;				// Value
		float E;				// Error
		bool D;					// Setpoint Reached (Val >= SP)
		bool LL;				// Low Low Signal (Val <= LLV)
		bool L;					// Low Signal (Val <= LV)
		bool H;					// High Signal (Val >= HV)
		bool HH;				// High High Signal (Val >= HHV)

		void Init();
		bool Ini;				// Initialize Module
};
#endif

