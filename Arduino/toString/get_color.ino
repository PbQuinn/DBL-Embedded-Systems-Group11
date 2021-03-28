

int getColor(int sensorPin, int colorRanges[]){
  float readings[sampleSize];
  float counterValue = 0;
  
  for(int i = 0; i < sampleSize; i++){
    Serial.print("Pin ");
    Serial.print(sensorPin);
    Serial.print(" reading: ");
    float readValue = analogRead(sensorPin);
    Serial.println(readValue);
    counterValue += readValue;
    readings[i] = readValue;
    delay(10);
  }

  float averageValue = counterValue/sampleSize;


  //After extensive testing, we know that color values for primary sensor are in ascending order:
  //Neither - Black - White
  if(averageValue > colorRanges[4] && averageValue <= colorRanges[5]){
    Serial.println("Found white!");
    return WHITE;
  }
  
  if(averageValue > colorRanges[2] && averageValue <= colorRanges[3]){
    Serial.println("Found black!");
    return BLACK;
  }

  if(averageValue > colorRanges[0] && averageValue <= colorRanges[1]){
    Serial.println("Found..... something else?");
    return NEITHER;
  }

  return NEITHER;

  
  


  
}
