/*Title: mjbWorld
   Copyright (c) 1998-2002 Martin John BakerThis program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General License
   as published by the Free Software Foundation; either version 2
   of the License, or (at your option) any later version.This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   GNU General License for more details.For information about the GNU General License see http://www.gnu.org/To discuss this program http://sourceforge.net/forum/forum.php?forum_id=122133
   also see website https://www.euclideanspace.com/
   */#include "mjbModel.h"/* x3d definition<!ENTITY % SFRotation "CDATA"> <!-- Rotation -->
   */sfrotation::sfrotation(double x1,double y1,double z1,double a1) {
   x=x1;
   y=y1;
   z=z1;
   angle=a1;
   saveAsDouble = false ;
   }sfrotation::sfrotation(sfrotation* in) {
   x=(in) ? in->x : 0;
   y= (in) ? in->y : 0;
   z= (in) ? in->z : 1;
   angle= (in) ? in->angle : 0;
   saveAsDouble = false ;
   }sfrotation::sfrotation() {
   saveAsDouble = false ;
   }String* sfrotation::vrmlType(){
   return "SFRotation";
   }property* sfrotation::clone() {
   //Console::WriteLine("sfparam::clone");
   return new sfrotation(this);
   }/** create an array of the appropriate type
   * with a size given by the parameter
   */
   property* sfrotation::createArray(int size)[]{
   return new sfrotation*[size];
   }sfrotation* sfrotation::minus() {
   return new sfrotation(x,y,z,-angle);
   }void sfrotation::set(double tx,double ty,double tz) {
   angle = Math::Sqrt(tx*tx + ty*ty + tz*tz);
   if (angle == 0) {x=1;y=z=0;return;}
   x = tx/angle;
   y = ty/angle;
   z = tz/angle;
   }void sfrotation::set(double tx,double ty,double tz,double tangle){
   x = tx;
   y = ty;
   z = tz;
   angle = tangle;
   }double sfrotation::getTx() {
   return x*angle;
   }double sfrotation::getTy() {
   return y*angle;
   }double sfrotation::getTz() {
   return z*angle;
   }void sfrotation::add(sfrotation* r) {
   double tx = (r->x * r->angle) + (x * angle);
   double ty = (r->y * r->angle) + (y * angle);
   double tz = (r->z * r->angle) + (z * angle);
   angle = Math::Sqrt(tx*tx + ty*ty + tz*tz);
   if (angle == 0) {x=1;y=z=0;return;}
   x = tx/angle;
   y = ty/angle;
   z = tz/angle;
   }/** get a single value
   * inst = instance number
   * nb = nodeBean this property is contained in - only used in case this is
   * in a PROTO and parameter has an IS value
   */
   property* sfrotation::get(int inst,nodeBean* nb) {
   return this;
   }String* sfrotation::ToString() {
   return String::Concat(S"(",__box(x)->ToString(),S",",
   __box(y)->ToString(),S",",
   __box(z)->ToString(),S",",
   __box(angle)->ToString(),S")");
   }/** output as a string
   * mode values
   * 0 - output modified values
   * 1 - output original values
   * 2 - output attribute
   * 3 - output attribute in brackets
   * 4 - output with f prefix
   */
   String* sfrotation::outstring(int format) {
   if (format == 3) {
   if (saveAsDouble)
   return String::Concat(S"(",__box(x),S" ",__box(y),S"    ",__box(z),S" ",__box(angle),S")");
   else
   return String::Concat(S"(",__box((float)x)->ToString(),S"    ",
   __box((float)y)->ToString(),S" ",
   __box((float)z)->ToString(),S" ",
   __box((float)angle)->ToString(),S")");
   } else if (format == 4) { // output to C
   return String::Concat(__box((float)angle)->ToString(),S"f *90/1.57,"    , // convert to degrees
   __box((float)x)->ToString() ,S"f," ,
   __box((float)y)->ToString() ,S"f," ,
   __box((float)z)->ToString() ,S"f");
   } else {
   if (saveAsDouble)
   return String::Concat(__box(x),S" ",__box(y),S" ",__box(z),S"    ",__box(angle));
   else
   return String::Concat(__box((float)x)->ToString(),S" ",
   __box((float)y)->ToString(),S" " ,
   __box((float)z)->ToString(),S" " ,
   __box((float)angle)->ToString());
   }
   }/** write to file
   * filter = information about output
   * mode values
   * 0 - output VRML97 modified values
   * 1 - output VRML97 original values
   * 2 - output xml (x3d)
   * 3 - output attribute in brackets
   * 4 - output with f prefix
   */
   void sfrotation::write(filter* f,int mode,int indent){
   f->write(outstring(mode));
   }/** used by mfparam->vrml2par
   */
   bool sfrotation::instring(filter* f,sfparam* sfp,nodeBean* n,int mode) {
   String* s;
   try {
   s=f->nextToken();
   if (s) if (s->Equals("IS")) {
   s=f->nextToken();
   if (sfp) sfp->setIs(s);
   return true;
   }
   x = Double::Parse(s);
   s=f->nextToken();
   y = Double::Parse(s);
   s=f->nextToken();
   z = Double::Parse(s);
   s=f->nextToken();
   angle = Double::Parse(s);
   } catch (Exception* e) {
   Console::WriteLine("sfrotation->instring error: {0}",e);
   }
   return true;
   }bool sfrotation::instring(filter* f,String* s1) {
   String* s;
   try {
   x = Double::Parse(s1);
   s=f->nextToken();
   y = Double::Parse(s);
   s=f->nextToken();
   z = Double::Parse(s);
   s=f->nextToken();
   angle = Double::Parse(s);
   } catch (Exception* e) {
   Console::WriteLine("sfrotation->instring error: {0}",e);
   }
   return true;
   }