

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
  //Serial.print("Testing value: ");
  //Serial.print(averageValue);
  //Serial.print(" against average ranges (b/w) (");
  //Serial.print(primary_ranges[0]);
  //Serial.print(", ");
  //Serial.print(primary_ranges[1]);
  //Serial.print(") (");
  //Serial.print(primary_ranges[2]);
  //Serial.print(", ");
  //Serial.print(primary_ranges[3]);
  //Serial.println(")");
  Serial.write(123);
  Serial.write((int) averageValue);
  //After extensive testing, we know that color values for primary sensor are in ascending order:
  //Neither - Black - White
  if(averageValue > colorRanges[2]){
    return WHITE;
  }
  
  if(averageValue > colorRanges[0] && averageValue <= colorRanges[1]){
    return BLACK;
  }

  return NEITHER;

  
  


  
}
