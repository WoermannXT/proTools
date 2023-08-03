/*
  CYC - Woermann Automation
  Cycle Clock Processing Class
  Created 2021-04-19
*/
#include <stdint.h>
#include <sys/time.h>

#ifndef CYC_h
#define CYC_h

		typedef struct {
			unsigned short ms;  		// Time Milliseconds
			unsigned short s;  			// Time Seconds
			unsigned short m;  			// Time Minutes
			unsigned short h;  			// Time Hours
			unsigned short d; 			// Time Days
		} CYC_TIM;						// Time Struct

		typedef struct {
			bool x2e : 1;  				// Every Even Cycle
			bool x2o : 1;  				// Every Odd Cycle
			bool x3 : 1;  				// Every Third Cycle
			bool x5 : 1;  				// Every Fith Cycle
			bool x7 : 1;  				// Every Seventh Cycle
			bool x11 : 1;  				// Every Eleventh Cycle
			bool x13 : 1;  				// Every Thirteenth Cycle
		} CYC_CYC;						// Cycle Slice Bit Struct

		typedef struct {
			bool x10ms : 1;  			// 10 ms Pulse 
			bool x100ms : 1;  			// 100 ms Pulse 
			bool x1s : 1;  				// 1 s Pulse 
			bool x6s : 1;  				// 6 s Pulse 
			bool x10s : 1;  			// 10 s Pulse 
			bool x60s : 1;  			// 60 s Pulse 
			bool x100s : 1;  			// 100 s Pulse 
		} CYC_CLK;						// Clock Bit Struct

		typedef struct {
			unsigned long m10ms; 	// Memory for 0.1 s Counter
			unsigned long m100ms; 	// Memory for 0.1 s Counter
			unsigned long m1s;  	// Memory for 1 s Counter
			unsigned long m6s;  	// Memory for 6 s Counter
			unsigned long m10s; 	// Memory for 10 s Counter
			unsigned long m60s; 	// Memory for 60 s Counter
			unsigned long m100s; 	// Memory for 100 s Counter
		} CYC_CLK_MEM;				// Clock Memory Struct

class CYC { 
	// Class Member Variables
	public:
		CYC();
		
		void Update( unsigned long _SysT);
		unsigned long SysT;			// System Time at Update
		unsigned long CycC;			// Cycle Counter
		unsigned long CycT;			// Previous Cycle Time in micros
		unsigned int CycPS;			// Cycles per second

		CYC_CYC cs;					// Cycle Slice Struct
		CYC_CLK cp;					// Clock Pulse Struct
		CYC_CLK ct;					// Clock Toggle Struct
		CYC_TIM ti;					// Time Struct
		CYC_CLK_MEM cm;				// Clock Memory

		void Init();				
		bool Ini;					// Initialize Module

		void SetTime( unsigned long _sSet, unsigned long _mSet, unsigned long _hSet, unsigned long _dSet );	// Set Time

	private:
		unsigned int iCycC;	
		unsigned int CycPSCnt;		// Cycles per second Counter


};
#endif
