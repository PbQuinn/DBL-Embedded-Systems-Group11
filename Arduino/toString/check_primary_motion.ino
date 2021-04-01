

bool checkPrimaryMotion(){
  int strikes = 0;
  // do we have a lot of outliers which would mean we have a disk
  for(int i = 0; i < sampleSize; i++){
    int sample = analogRead(primaryMotionSensor);
    if(belt_range[0] > sample){
      strikes++;
    }
    if(strikes >= 3){
      return true;
    }
  }
  return false;
}