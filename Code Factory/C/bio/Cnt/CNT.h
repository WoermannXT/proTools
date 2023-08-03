/*
  CNT - Woermann Automation
  Counter Processing Class
  Created 2021-04-12
*/
#ifndef CNT_h
#define CNT_h

class CNT { 
	// Class Member Variables
	public:
		CNT(float _Fact, uint8_t _Type);
		float Fact;				// Factor for Counter Value to Process Value
		uint8_t Type;			// Counter Type, 0 = Count when Positive Edge; 1 = Count when Negative Edge; 2 = Count when True; 3 = Count when False;

		float Update(bool _Raw, bool _Down);
		bool Raw;				// Raw Signal Memory
		long Cnt;				// Counter Value
		float Val;				// Processed Counter Value (Cnt * Fact)

		float UpdateByVal(float _RawVal, bool _Down);
		bool RawVal;			// Raw Value Memory
		bool RawD;				// Raw Value Delta / Difference
		
		void Init();
		bool Ini;				// Initialize Module

};
#endif
