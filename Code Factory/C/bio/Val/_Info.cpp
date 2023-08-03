
// Define VAL
// Altitude Sensor using BMP280
VAL Altitude(0, 4096, 0, 10000, 1,); // Input Min, Input Max, Out Min, Out Max, Type

// Update VAL
altival = Altitude.Update(/*Raw Value*/ analogRead(0)); // Raw Value



