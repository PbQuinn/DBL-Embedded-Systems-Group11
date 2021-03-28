

boolean rangemaker(int lowest, int middle, int highest, int arrayrange[]) {
  int lowerrange = (middle - lowest);
  Serial.print("LOWER DIFF:");
  Serial.println(lowerrange);
  if(lowerrange < 12){
    return false;
  }else if(lowerrange > 100){
    arrayrange[0] = max(lowest - lowerrange/5,0);
    arrayrange[1] = lowest + lowerrange/5;
    arrayrange[2] = middle - lowerrange/5;
    arrayrange[3] = middle + lowerrange/5;
  }else{
    arrayrange[0] = max(lowest - 10,0);
    arrayrange[1] = lowest + 6;
    arrayrange[2] = middle - 6;
    arrayrange[3] = middle + 6;
  }
  int upperrange =  (highest - middle);
  Serial.print("UPPER DIFF:");
  Serial.println(upperrange);
  if(upperrange < 20){
    return false;
  }else if(upperrange > 100){
    arrayrange[4] = highest - upperrange/5;
    arrayrange[5] = highest + upperrange/5;
  }else{
    arrayrange[4] = highest - 10;
    arrayrange[5] = highest + 10;
  }
  return true;  
}
