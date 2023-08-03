/*
  PID - Woermann Automation
  PID Processing Class
  Created 2019-12-03
*/

#ifndef PID_h
#define PID_h

class PID { 
	// Class Member Variables
	public:
		PID(float _Kp, float _Ki, float _Kd, float _OMin, float _OMax, float _OIni, float _TBase, bool _Inv);
		float Kp;			// Proportional Gain
		float Ki;			// Integral Gain
		float Kd;			// Derivative Gain	
		float OMin;			// Output Minimum
		float OMax;			// Output Maximum
		float OIni;			// Initial Output Value (if COn is false)
		float TBase;		// PID Update Time in Seconds
		bool Inv;			// Inverse Control Logic
		
		float Update(float _Set, float _Val, bool _On);
		float UpdatePI(float _Set, float _Val, bool _On);
		float UpdateP(float _Set, float _Val, bool _On);
		float UpdateSO(float _Set, float _Val, bool _On);
		float Out;			// Output Value
		float E;			// PID Error
		float sPID;			// Proportionat Part + Integral Part + Differential Part
		float Val;			// Process Value

		void Init(float _OIni);		// Initialise Control Object
		bool Ini;					// Initialize Module
		void SetKp(float _Kp);		// Set/Update P Value Factor
		void SetKi(float _Ki);		// Set/Update I Value Factor
		void SetKd(float _Kd);		// Set/Update D Value Factor
		void PreSense(float _PSV, float _Fact);	// Update Value with Factor
		float PSV;								// Pre-Sense Value

	private:
		float E1;			// PID Error Saved
		float dPV;			// Delta Process Value
		float dPV1;			// Delta Process Value Saved
};
#endif
