/*
  STA.h - Woermann Automation
  Statistics Processing Class
  Created 2020-01-08.
*/

#ifndef STA_h
#define STA_h

class STA {
  // Class Member Variables
  public:
	STA();

	void Update(float _Val);
	float Val;				// Value
	float Min;				// Minimum Value
	float Max;				// Maximum Value
	float Avg;				// Average Value
	
	void Init(float _Val);
	bool Ini;				// Initialize Module

	private:
	uint32_t AvgCnt;		// Average Value Counter
   };
#endif

