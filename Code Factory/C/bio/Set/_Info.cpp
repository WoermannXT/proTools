
// Define SET
// SET(float SP, float LLV, float LV, float HV, float HHV)
// SP = Setpoint
// LLV = Low Low Value
// LV = Low Value
// HV = High Value
// HHV = High High Value
SET setAirS( 3.0f, 2.0f, 2.5f, 3.5f, 10.0f); 

// Update SET
SpeedD = setSpeed.Update( analogRead(0)); // Raw Value, Reset Stats

