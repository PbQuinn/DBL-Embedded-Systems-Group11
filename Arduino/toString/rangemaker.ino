
boolean rangemaker(int lowest, int highest, int arrayrange[]) {
  int difference = (highest - lowest);
  if(difference < 20){
    Serial.println("difference too small!");
    Serial.println(SETUP_FAIL);
    return false;
  }else {
    arrayrange[0] = lowest - 10;
    arrayrange[1] = lowest + 10;
    arrayrange[2] = highest - 10;
    arrayrange[3] = highest  + 10;
    return true;
  }
}
