

bool checkSecondaryMotion(){
  int strikes = 0;

  for(int i = 0; i < 5*sampleSize; i++){
    int sample = analogRead(secondaryColorSensor);
    if(sample > funnel_range[1]){
      strikes++;
    }
    if(strikes >= 4*sampleSize){
      return true;
    }
  }
  return false;
}
