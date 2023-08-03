
// Define TIM
TIM timS1(12.3f, 1); // Setpoint, Type (0 = Microsecond Timer; 1 = Millisecond Timer; 2 = Second Timer; 3 = Minute Timer; 4 = Hour Timer)

// Update TIM
timS1.Update(CycT); // Cycle Time mesured by CYC

if (seq1.SStFC) {
	timS1.Sp = 300 //ms
}
timS1.S = true;	// Start Timer
timS1.P = !Motor.On;

if (Reset) {
	S1StepTime.Reset();	// Reset Timer
}




