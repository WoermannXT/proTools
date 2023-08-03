
// Define PID Control Loop
PID pid1(1, 1, 1, 0, 100, 50); // Kp, Ki, Kd, OMin, OMax, StartVal

// Update PID Controller
Serv1 = pid1.Update( Setpoint, Value, true); // (SetP, PVal, COn)





  
  Autotune:
	Res (Response Factor)  = AV/AO (Amplitude Value / Amplitude Output)
	Tim (Time Delay) = (P2P+L2L)/2 
			Kp			Ki			Kd
	PID		3/Res		6Tim/Res		Tim/12Res
  
PID Autotune

 	
	bool AutoTune();
	bool ATRequest;		// Auto Tune Request
	bool ATActive;		// Auto Tune Active
	bool ATDone;		// Auto Tune Done
	double TimerV;		// Timer Value
	int Step;			// Step No.
	int SubStep;		// Sub Step No.
	float PValF;		// Filtered Output Value
	float OValF;		// Filtered Process Value
	float RTOff;		// Response Test Offset
	float AO;			// Amplitude Output
	float AV;			// Amplitude Value
	float P2P;			// Time Peak to Peak 
	float L2L;			// Time Low to Low 
	float Tim;			// Peak to Peak 
	float NBand;		// Noise Band for Cross Detection
	float LBack;		// Noise Time for Peak/Low Detection


/*
1. Init 
	set Static Output?
	read Process Value and build Average
	read Noise (Variance)
2. Test
	run Test
3. Calculate / Set Parameters
*/
bool PID::AutoTune() {
	if (!ATDone) ATRequest = true;
	return ATDone;
}

void AutoTuneRun() {
	switch (Step)
	{
	// Initialise --------------------------------------
	case 1: 
		ORange = _OMax - _OMin; // Get Output Range
		PValF = PVal;			// Reset Filtered Process Value
		OValF = OVal;			// Reset Filtered Output Value
		RTOff = 0.0;			// Reset Offset
		TimerV = 0;				// Reset Timer
		Step ++;				// GoTo Next Step
		break;
	// Get Standard Values ------------------------------
	case 2: 
		PValF * 0.05 + (PValF * 0.95);
		if (COn) {
			TimerV += TBase;
		}
		else {
			TimerV = 0;
		}
		if (TimerV >= 1000) {
			TimerV = 0;			// Reset Timer
			Step ++;			// GoTo Next Step
		}
		break;
	// Test PID Reponse---------------------------------
	case 3: // test to max 25% of ORange
		TimerV += TBase;
		switch (SubStep)
		{
		// Positive Offset 1 ----------------------------
		case 1:
			/* code */
			break;
		// Nagative Offset 1 ----------------------------
		case 2:
			/* code */
			break;
		// Positive Offset 2 ----------------------------
		case 3:
			/* code */
			break;
		// Nagative Offset 2 ----------------------------
		case 4:
			/* code */
			break;
		
		default:
			break;
		}

		break;
	// Calculate PID Parmeters -------------------------
	case 4: // Calculate PID Parmeters
		TimerV += TBase;
		if (TimerV >= 1000) {
			Step ++;
			TimerV = 0;
		}
		break;
	
		if (TimerV >= 1000) {
			Step = 1;
		}
		TimerV = 0;
	// Ready -------------------------------------------
	default:
		break;
	// End ---------------------------------------------
	}
	float x = OVStatic;
}
