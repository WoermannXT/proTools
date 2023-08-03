/*
  TIM - Woermann Automation
  Timer Processing Class
  Created 2021-04-12
*/
#ifndef TIM_h
#define TIM_h

	class TIM { 
	// Class Member Variables
	public:
		TIM(float _Set, char _Type);
	    float Set;				// Setpoint to Type selection
		char Type;			// Timer Type, 0 = Millisecond Timer; 1 = Second Timer; 2 = Minute Timer; 3 = Hour Timer;

		bool Update(unsigned long _CycT);
		unsigned long Tim;			// Timer Value
		float Val;				// Processed Timer Value to Type selection
		bool D;					// Setpoint Reached (Val >= SP)
		bool S;					// Timer Start Counting, Reset Tim and Val to 0 if False
		bool P;					// Timer Pause Counting (internaly reset, has to be continuesly set to pause)
		bool R;					// Timer Reset (internaly reset)
		
		void Init();
		bool Ini;				// Initialize Module

	private:

	};
#endif
