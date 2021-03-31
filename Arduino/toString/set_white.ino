

int setWhite(){
    closeBlocker();
    waitTime(3000);   
    int primaryWhiteMeasured = setWhiteForSensor(primaryColorSensor);
    int secondaryWhiteMeasured = setWhiteForSensor(secondaryColorSensor);
    openBlocker();
    stringDisk();
    BeltMotor->run(FORWARD);
    waitTime(1000);
    BeltMotor->run(RELEASE);
  
  if(primaryWhiteMeasured > 0 && secondaryWhiteMeasured > 0){
       primary_white = primaryWhiteMeasured;
       secondary_white = secondaryWhiteMeasured;
    return CONFIRM_SET_WHITE;
  } else {
    return SETUP_FAIL;
  }
}

int setWhiteForSensor(int sensorPin){
  float readings[sampleSize];
  float counterValue = 0;
  
  for(int i = 0; i < sampleSize; i++){
    float readValue = analogRead(sensorPin);
    counterValue += readValue;
    readings[i] = readValue;
    waitTime(10);
  }

  float averageValue = counterValue/sampleSize;

  for(int i = 0; i < sampleSize; i++){
    if(readings[i] - averageValue > consistencyLimit || readings[i] - averageValue < -consistencyLimit){
      return SETUP_FAIL;
    }
  }
  
  return averageValue;
}
