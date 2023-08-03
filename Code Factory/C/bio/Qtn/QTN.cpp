/*
  QTN - Woermann Automation
  Quaternion Processing Class
  Created by EWo, 2021-04-19

  Info:
http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/index.htm

  ToDo:
	
*/

#include <math.h>
#include "QTN.h"

// Constructor-------------------------------------------------------------------------------------
/*!
 *  @brief	Set up the QTN Module
 * 
 *  @return  none
 */
QTN::QTN() {
	Init();
}
// QTN Algorithm ----------------------------------------------------------------------------------
/*!
 *  @brief	Update the QTN Module, this should be done at an interval rate of the defined time base in the constructor
 *  @param 	_SysT
 *			System Time im microseconds
 *  @return none
 */

// http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/code/index.htm
// Conjugate
Quaternion QTN::Conj(Quaternion _Q1) {
	Q.x = -_Q1.x;
	Q.y = -_Q1.y;
	Q.z = -_Q1.z;
	Q.w = _Q1.w;

	return Q;

} 
// Normalise Quaternions
Quaternion QTN::Norm(Quaternion _Q1) {
	float n = Math.sqrt(_Q1.x*_Q1.x + _Q1.y*_Q1.y + _Q1.z*_Q1.z + _Q1.w*_Q1.w);
	if (n==0) {
	Q.w = 0;
	Q.x = 0;
	Q.y = 0;
	Q.z = 0;
	}
	else {
	Q.w = _Q.w / n;
	Q.x = _Q.x / n;
	Q.y = _Q.y / n;
	Q.z = _Q.z / n;
	}

	return Q;
	} 
// Scale Quaternions
Quaternion QTN::Scale(float _s) {
	Q.x *= _s;
	Q.y *= _s;
	Q.z *= _s;
	Q.w *= _s;

	return Q;
} 
// Multiply Quaternions
Quaternion QTN::Mul(Quaternion _Q1, Quaternion _Q2) {
	Q.x =  _Q1.x * _Q2.w + _Q1.y * _Q2.z - _Q1.z * _Q2.y + _Q1.w * _Q2.x;
	Q.y = -_Q1.x * _Q2.z + _Q1.y * _Q2.w + _Q1.z * _Q2.x + _Q1.w * _Q2.y;
	Q.z =  _Q1.x * _Q2.y - _Q1.y * _Q2.x + _Q1.z * _Q2.w + _Q1.w * _Q2.z;
	Q.w = -_Q1.x * _Q2.x - _Q1.y * _Q2.y - _Q1.z * _Q2.z + _Q1.w * _Q2.w;
	
	return Q;
} 
// Add Quaternions
Quaternion QTN::Add(Quaternion _Q1, Quaternion _Q2) {
    Q.x = _Q1.x + _Q2.x;
    Q.y = _Q1.y + _Q2.y;
    Q.z = _Q1.z + _Q2.z;
    Q.w = _Q1.w + _Q2.w;
	
	return Q;
} 

// Quarternions to Euler Angles (normalized)
//http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToEuler/index.htm
void Q2En(Quat4d _Q1) {
	float test = _Q1.x * _Q1.y + _Q1.z * _Q1.w;
	if (test > 0.499) { // singularity at north pole
		heading = 2 * atan2(_Q1.x, _Q1.w);
		attitude = Math.PI / 2;
		bank = 0;
		return;
	}
	if (test < -0.499) { // singularity at south pole
		heading = -2 * atan2(_Q1.x,_Q1.w);
		attitude = - Math.PI/2;
		bank = 0;
		return;
	}
    float sqx = _Q1.x*_Q1.x;
    float sqy = _Q1.y*_Q1.y;
    float sqz = _Q1.z*_Q1.z;
    heading = atan2(2*_Q1.y*_Q1.w-2*_Q1.x*_Q1.z , 1 - 2*sqy - 2*sqz);
	attitude = asin(2*test);
	bank = atan2(2*_Q1.x*_Q1.w-2*_Q1.y*_Q1.z , 1 - 2*sqx - 2*sqz)
}

// Quarternions to Euler Angles (can be non normalized)
void Q2Enn(Quat4d q1) {
    float sqw = q1.w*q1.w;
    float sqx = q1.x*q1.x;
    float sqy = q1.y*q1.y;
    float sqz = q1.z*q1.z;
	float unit = sqx + sqy + sqz + sqw; // if normalised is one, otherwise is correction factor
	float test = q1.x*q1.y + q1.z*q1.w;
	if (test > 0.499*unit) { // singularity at north pole
		heading = 2 * atan2(q1.x,q1.w);
		attitude = Math.PI/2;
		bank = 0;
		return;
	}
	if (test < -0.499*unit) { // singularity at south pole
		heading = -2 * atan2(q1.x,q1.w);
		attitude = -Math.PI/2;
		bank = 0;
		return;
	}
    heading = atan2(2*q1.y*q1.w-2*q1.x*q1.z , sqx - sqy - sqz + sqw);
	attitude = asin(2*test/unit);
	bank = atan2(2*q1.x*q1.w-2*q1.y*q1.z , -sqx + sqy - sqz + sqw)
}

//http://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToQuaternion/index.htm
// First method
void E2Q(float heading, float attitude, float bank) {
    // Assuming the angles are in radians.
    float c1 = Math.cos(heading/2);
    float s1 = Math.sin(heading/2);
    float c2 = Math.cos(attitude/2);
    float s2 = Math.sin(attitude/2);
    float c3 = Math.cos(bank/2);
    float s3 = Math.sin(bank/2);
    float c1c2 = c1*c2;
    float s1s2 = s1*s2;
    w =c1c2*c3 - s1s2*s3;
  	x =c1c2*s3 + s1s2*c3;
	y =s1*c2*c3 + c1*s2*s3;
	z =c1*s2*c3 - s1*c2*s3;
  }


// https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles


Quaternion ToQuaternion(float yaw, float pitch, float roll) // yaw (Z), pitch (Y), roll (X)
{
    // Abbreviations for the various angular functions
    float cy = cos(yaw * 0.5);
    float sy = sin(yaw * 0.5);
    float cp = cos(pitch * 0.5);
    float sp = sin(pitch * 0.5);
    float cr = cos(roll * 0.5);
    float sr = sin(roll * 0.5);	

    Quaternion q;
    Q.w = cr * cp * cy + sr * sp * sy;
    Q.x = sr * cp * cy - cr * sp * sy;
    Q.y = cr * sp * cy + sr * cp * sy;
    Q.z = cr * cp * sy - sr * sp * cy;

    return Q;
}



EulerAngles ToEulerAngles(Quaternion _Q1) {
    EulerAngles angles;

    // roll (x-axis rotation)
    float sinr_cosp = 2 * (q.w * q.x + q.y * q.z);
    float cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y);
    angles.roll = std::atan2(sinr_cosp, cosr_cosp);

    // pitch (y-axis rotation)
    float sinp = 2 * (q.w * q.y - q.z * q.x);
    if (std::abs(sinp) >= 1)
        angles.pitch = std::copysign(M_PI / 2, sinp); // use 90 degrees if out of range
    else
        angles.pitch = std::asin(sinp);

    // yaw (z-axis rotation)
    float siny_cosp = 2 * (q.w * q.z + q.x * q.y);
    float cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z);
    angles.yaw = std::atan2(siny_cosp, cosy_cosp);

    return angles;
}



// https://www.cbcity.de/tutorial-rotationsmatrix-und-quaternion-einfach-erklaert-in-din70000-zyx-konvention
/*/ Python Implementierung für Rotationsmatrix nach ZYX Konvention
def Rypr(y, p, r){
//	Rotationsmatrix für y=yaw, p=pitch, r=roll in degrees

    // from Degree to Radians
    y = y * QTN_PI / 180.0;
    p = p * QTN_PI / 180.0;
    r = r * QTN_PI / 180.0;
	
	todo >
    Rr = np.matrix([[1.0, 0.0, 0.0],[0.0, np.cos(r), -np.sin(r)],[0.0, np.sin(r), np.cos(r)]])
    Rp = np.matrix([[np.cos(p), 0.0, np.sin(p)],[0.0, 1.0, 0.0],[-np.sin(p), 0.0, np.cos(p)]])
    Ry = np.matrix([[np.cos(y), -np.sin(y), 0.0],[np.sin(y), np.cos(y), 0.0],[0.0, 0.0, 1.0]])
 
    return Ry*Rp*Rr
} //*/

def normQ(Quaternion _Q1){
//	Calculates the normalized Quaternion
//	a is the real part
//	b, c, d are the complex elements'''
    // Source: Buchholz, J. J. (2013). Vorlesungsmanuskript Regelungstechnik und Flugregler.
    // GRIN Verlag. Retrieved from http://www.grin.com/de/e-book/82818/regelungstechnik-und-flugregler

	// Betrag
	float n = Math.sqrt(_Q.w*_Q.w + _Q.x*_Q.x + _Q.y*_Q.y + _Q.z*_Q.z);

	Q.w = _Q1.w / Z;
	Q.x = _Q1.x / Z;
	Q.y = _Q1.y / Z;
	Q.z = _Q1.z / Z;

    return Q
}

def QtoR(Quaternion _Q1):
    '''Calculates the Rotation Matrix from Quaternion
    a is the real part
    b, c, d are the complex elements'''
    # Source: Buchholz, J. J. (2013). Vorlesungsmanuskript Regelungstechnik und Flugregler.
    # GRIN Verlag. Retrieved from http://www.grin.com/de/e-book/82818/regelungstechnik-und-flugregler
    q = normQ(q)
 
    a, b, c, d = q
 
    R11 = (a**2+b**2-c**2-d**2)
    R12 = 2.0*(b*c-a*d)
    R13 = 2.0*(b*d+a*c)
 
    R21 = 2.0*(b*c+a*d)
    R22 = a**2-b**2+c**2-d**2
    R23 = 2.0*(c*d-a*b)
 
    R31 = 2.0*(b*d-a*c)
    R32 = 2.0*(c*d+a*b)
    R33 = a**2-b**2-c**2+d**2
 
    return np.matrix([[R11, R12, R13],[R21, R22, R23],[R31, R32, R33]])






def Q2Eul(q):
    '''Calculates the Euler Angles from Quaternion
    a is the real part
    b, c, d are the complex elements'''
    # Source: Buchholz, J. J. (2013). Vorlesungsmanuskript Regelungstechnik und Flugregler.
    # GRIN Verlag. Retrieved from http://www.grin.com/de/e-book/82818/regelungstechnik-und-flugregler
    q = normQ(q)
 
    a, b, c, d = q
 
    gieren = np.arctan2(2.0*(b*c+a*d),(a**2+b**2-c**2-d**2)) * 180.0/np.pi
    nicken = np.arcsin(2.0*(a*c-b*d)) * 180.0/np.pi
    wanken = -np.arctan2(2.0*(c*d+a*b),-(a**2-b**2-c**2+d**2)) * 180.0/np.pi
 
    return np.array([gieren, nicken, wanken])



// Initialise -------------------------------------------------------------------------------------
/*!
 *  @brief	Initialize QTN Variables
 *  @return none
 */
void QTN::Init() {
	Ini = true;
}

