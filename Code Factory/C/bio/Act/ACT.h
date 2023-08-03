/*
  ACT.h - Woermann Automation
  Actuator Processing Class
  Created 2021-04-12
*/
#ifndef ACT_h
#define ACT_h

class ACT { 
	// Class Member Variables
	public:
		ACT(uint32_t _TOnSet, uint32_t _TOffSet, uint32_t _TAlSet, uint8_t _Type);
		uint32_t TOnSet;		// Timer Setpoint On in Microseconds
		uint32_t TOffSet;		// Timer Setpoint Off in Microseconds
		uint32_t TOVal;			// Timer Value On/Off in Microseconds
		uint32_t TAlSet;		// Timer Setpoint for Alarm in Microseconds
		uint32_t TAlVal;		// Timer Value for Alarm in Microseconds
		bool Type;				// Type 0 = No Feedback, 1 = Off Feedback, 3 = On Feedback

		bool Update(uint32_t _CycT);
		bool Fba;				// Feedback Signal
		bool Out;				// Processed Output On
		bool COn;				// Control On, if False Control Off
		bool FOn;				// Feedback On (Response to COn)
		bool GAl;				// General Alarm
		bool posP;				// Switching positive Pulse
		bool negP;				// Switching negative Pulse
		
		void Init();
		bool Ini;				// Initialize Module

	private:
	
};
#endif

