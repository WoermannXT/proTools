/*
  SEQ.h - Woermann Automation
  Sequence Processing Class
  Created 2020-04-12
*/
#ifndef SEQ_h
#define SEQ_h

class SEQ { 
	// Class Member Variables
	public:
		SEQ(char _StepMap[16]);
		char StepMap[16];	// Sequence Step Map

		char Update();
		bool SStA;	 			// Sequence Step Active (READ)
		bool SStFC;				// Sequence Step First Cycle (READ)
		bool SStD;				// Sequence Step Done (WRITE)
		bool SSt0;				// Sequence in Step 0
		char SStID;			// Sequence Step ID
		char SStIDNext;		// Sequence Step ID Next
		char SStNo;			// Sequence Step Number
		char SStNoNext;		// Sequence Step Number Next

		void Init();
		bool Ini;				// Initialize Module
};
#endif

