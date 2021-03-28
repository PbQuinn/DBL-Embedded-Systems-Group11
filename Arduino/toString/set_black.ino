

int setBlack(){
    closeBlocker();
    delay(3000);
    BeltMotor->run(RELEASE);    
    int primaryBlackMeasured = setBlackForSensor(primaryColorSensor);
    int secondaryBlackMeasured = setBlackForSensor(secondaryColorSensor);
    openBlocker();
    stringDisk();
    BeltMotor->run(FORWARD);
    delay(1000);
    BeltMotor->run(RELEASE);
  
  if(primaryBlackMeasured > 0 && secondaryBlackMeasured > 0){
       primary_black = primaryBlackMeasured;
       secondary_black = secondaryBlackMeasured;
    return CONFIRM_SET_BLACK;
  } else {
    return SETUP_FAIL;
  }
}

int setBlackForSensor(int sensorPin){
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
  Serial.print("Read average ");
  Serial.println(averageValue);

  for(int i = 0; i < sampleSize; i++){
    if(readings[i] - averageValue > consistencyLimit || readings[i] - averageValue < -consistencyLimit){
      Serial.print("Pin ");
      Serial.print(sensorPin);
      Serial.println(" detected outlier, color set failed");
      return SETUP_FAIL;
    }
  }
  Serial.print("No outliers detected, black assigned: " );
  Serial.print(averageValue);
  Serial.print(" for pin ");
  Serial.println(sensorPin);
  
  return averageValue;
}
