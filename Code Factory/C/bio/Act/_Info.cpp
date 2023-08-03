// ------------------------------------------------------------------------------------------------
// Define ACT
ACT Motor1(10, 100, 5, 3); // Push Button 1 // TOn, TOff, TAl, Type (Type 0= No Feedback, 1=Off Feedback, 3=On Feedback)


// ------------------------------------------------------------------------------------------------
// Update ACT
Motor1.Fba = DigitalPin(1);
M1Output = Motor1.Update( cyc1.CycT); // Millisecont Time Base

// ------------------------------------------------------------------------------------------------
// Motor Control On
Motor1.COn = Switch1.On
