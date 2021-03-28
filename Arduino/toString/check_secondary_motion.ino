

bool checkSecondaryMotion(){
  float readings[sampleSize];
  float counterValue = 0;
  
  for(int i = 0; i < sampleSize; i++){
    int sample = analogRead(secondaryColorSensor);
    bool sampleIsBlack = sample > secondary_ranges[2] && sample < secondary_ranges[3];
    bool sampleIsWhite = sample > secondary_ranges[4] && sample < secondary_ranges[5]; 
    if(!(sampleIsBlack || sampleIsWhite)){
      return false;
    }
  }
  return true;
}
