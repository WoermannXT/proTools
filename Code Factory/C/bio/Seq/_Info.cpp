// ------------------------------------------------------------------------------------------------
// Define SEQ (Initialize Flight Controller)

char StepMap[16] =  { 0,  // Idle
         1, // Init Sensor BMP280
         2, // Init Sensor BNO055 9DOF
         3, // Init Sensor NEO-M8 GPS
         4, // Init PIDs
         5, // Init Mixer
         6, // Start Motors 1 & 3
         7, // Start Motors 2 & 4
         8, // Initialisation Done
         0, // Idle
         };
SEQ seqMain(StepMap);

// ------------------------------------------------------------------------------------------------
// Update SEQ
switch (seq1.Update()) {
	case 0:			// Idle
		/* code */
		seq1.SStD = sigPB1.Sig;
	break;
	case 1:			// Init Sensor BMP280
		if (seq1.SStFC) {
			timS1.Sp = 300 //ms
		}
		/* code */
		seq1.SStD = ...;
	break;
	case 2:			// Init Sensor BNO055 9DOF
		/* code */
		seq1.SStD = ...;
	break;
	case 3:			// Init Sensor NEO-M8 GPS
		/* code */
		seq1.SStD = ...;
	break;
	case 4:			// Init PIDs
		/* code */
		seq1.SStD = ...;
	break;
	case 5:			// Init Mixer
		/* code */
		seq1.SStD = ...;
	break;
	case 6:			// Start Motors 1 & 3
		/* code */
		seq1.SStD = ...;
	break;
	case 7:			// Start Motors 2 & 4
		/* code */
		seq1.SStD = ...;
	break;
	case 8:			// Initialisation Done
		/* code */
		seq1.SStD = false;
	break;
}
if (Reset){
	seq1.Init()
}

