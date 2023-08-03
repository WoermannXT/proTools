
// Define SIG
SIG PushB1(10, 100, false); // Push Button 1 // TOn, TOff, Inverse

// Update SIG
SStD = PushB1.Update(digitalRead(0)); // RawSig

