/*
  QTN - Woermann Automation
  QTNle Clock Processing Class
  Created by EWo, 2021-04-19
*/

#ifndef QTN_h
#define QTN_h
#define QTN_PI 3.14159265358979323846 

class QTN { 
	// Class Member Variables
	public:
		QTN();
			
		struct EulerAngles {
			float roll, pitch, yaw;
		};
		struct Quaternion {
			float w, x, y, z;
		};

		void Update( Quaternion _Q);
		Quaternion Q;				// Quarternion Struct
		EulerAngles V;					// Vector Struct


		void Init();				
		bool Ini;					// Initialize Module

		void SetTime( unsigned long _sSet, unsigned long _mSet, unsigned long _hSet, unsigned long _dSet );	// Set Time

	private:
		int iQTNC;	
		int QTNPSCnt;				// QTNles per second Counter


};
#endif
