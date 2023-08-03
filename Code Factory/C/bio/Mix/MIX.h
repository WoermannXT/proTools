/*
  MIX.h - Woermann Automation Library.
  Created 2019-12-20.
*/
#ifndef MIX_h
#define MIX_h

typedef struct {
  int16_t S1;  // Rotor 1 CW Setpoint (front left)
  int16_t S2;  // Rotor 2 CCW Setpoint (front right)
  int16_t S3;  // Rotor 3 CW Setpoint (rear right)
  int16_t S4;  // Rotor 4 CCW Setpoint (raer left)
} _MixQuad;

class MIX { 
  // Class Member Variables
  public:
	MIX(int _ChMax, int _ChMin);
		int ChMax;		// Channel Maximum Output (for compensating)
		int ChMin;		// Channel Minimum Output (for compensating)
		float PGain;	// Pitch Gain
		float RGain;	// Roll Gain
		float YGain;	// Yaw Gain
		float TGain;	// Throttle Gain


	void UpdateQX(float _Pitch, float _Roll, float _Yaw,  float _Throttle,);
	void UpdateQP(float _Pitch, float _Roll, float _Yaw,  float _Throttle,);
	void UpdateVT(float _Pitch, float _Roll, float _Yaw,  float _Throttle,);
		_MixQuad Out;		// Mixed Outputs for Quad

		float Pitch;	// Compensated Pitch Setpoint
		float Roll;		// Compensated Roll Setpoint
		float Yaw;		// Compensated Yaw Setpoint
		float Throttle;	// Compensated Throttle Setpoint

	void Init();
	bool Ini;				// Initialize Module
	
	private:
	
};
#endif

