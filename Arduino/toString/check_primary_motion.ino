

bool checkPrimaryMotion(){
  float readings[sampleSize];
  float counterValue = 0;
  
  for(int i = 0; i < sampleSize; i++){
    int sample = analogRead(primaryColorSensor);
    
    if(primary_neither - sample > 50 || primary_neither - sample < -50){
      return true;
    }
  }
  return false;
}
