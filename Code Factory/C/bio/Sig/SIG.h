/*
  SIG.h - Woermann Automation
  Signal Processing Class
  Created 2019-12-03
*/
#ifndef SIG_h
#define SIG_h

class SIG { 
	// Class Member Variables
	public:
		SIG(unsigned long _TOn, unsigned long _TOff, bool _Inv);
		unsigned long TOnSet;		// Timer On in Microseconds
		unsigned long TOffSet;		// Timer Off in Microseconds
		unsigned long TOVal;			// Timer On/Off Value in Microseconds
		bool Inv;				// Signal Inverse

		bool Update(bool _Raw, unsigned long _CycT);
		bool Raw;				// Raw Signal
		bool Sig; 				// Processed Signal
		bool posP;				// Switching positive Pulse
		bool negP;				// Switching negative Pulse

		void Init();
		bool Ini;				// Initialize Module		
		
	private:

};
#endif

