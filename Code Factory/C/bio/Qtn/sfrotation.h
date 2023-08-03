/*Title: mjbWorld
   Copyright (c) 1998-2007 Martin John BakerThis program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General public: License
   as published by the Free Software Foundation; either version 2
   of the License, or (at your option) any later version.This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   GNU General public: License for more details.For information about the GNU General public: License see http://www.gnu.org/To discuss this program http://sourceforge.net/forum/forum.php?forum_id=122133
   also see website https://www.euclideanspace.com/
   */__gc class sfrotation : public property {
   public: static bool saveAsDouble = false ;
   public: double x;
   public: double y;
   public: double z;
   public: double angle;
   // VRML only supports float but allow override if higher resolution required public: sfrotation(double x1,double y1,double z1,double a1); public: sfrotation(sfrotation* in); public: sfrotation(); public: String* vrmlType(); public: static String* vrmlType_s(){
   return "SFRotation";
   } public: property* clone(); /** create an array of the appropriate type
   * with a size given by the parameter
   */
   public: property* createArray(int size)[]; public: sfrotation* minus(); public: void set(double tx,double ty,double tz); public: double getTx(); public: double getTy(); public: double getTz(); public: void add(sfrotation* r); /** get a single value
   * inst = instance number
   * nb = nodeBean this property is contained in - only used in case this is
   * in a PROTO and parameter has an IS value
   */
   public: property* get(int inst,nodeBean* nb);// public: void set(property* in,int inst);
   public: void set(double x,double y,double z,double angle); public: String* ToString();/** output as a string
   * mode values
   * 0 - output modified values
   * 1 - output original values
   * 2 - output attribute
   * 3 - output attribute in brackets
   * 4 - output with f prefix
   */
   public: String* outstring(int format);/** write to file
   * filter = information about output
   * mode values
   * 0 - output VRML97 modified values
   * 1 - output VRML97 original values
   * 2 - output xml (x3d)
   * 3 - output attribute in brackets
   * 4 - output with f prefix
   */
   public: void write(filter* f,int mode,int indent); /** used by mfparam.vrml2par
   */
   public: bool instring(filter* f,sfparam* sfp,nodeBean* n,int mode); public: bool instring(filter* f,String* s1); public: static Type* getEditClass(){
   return __typeof(sfrotationEditor);
   }
   };