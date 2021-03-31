

int getColor(int sensorPin, int colorRanges[]){
  
  float readings[sampleSize];
  float counterValue = 0;
  
  for(int i = 0; i < sampleSize; i++){
    float readValue = analogRead(sensorPin);
    counterValue += readValue;
    readings[i] = readValue;
    waitTime(10);
  }

  float averageValue = counterValue/sampleSize;

  //After extensive testing, we know that color values for primary sensor are in ascending order:
  //Neither - Black - White
  if(averageValue > colorRanges[2] && averageValue <= colorRanges[3]){
    return WHITE;
  }
  
  if(averageValue > colorRanges[0] && averageValue <= colorRanges[1]){
    return BLACK;
  }

  return NEITHER;

  
  


  
}
