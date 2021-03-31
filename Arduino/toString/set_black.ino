

int setBlack(){
    // set the black color also move the disks.
    closeBlocker();
    waitTime(3000); 
    int primaryBlackMeasured = setBlackForSensor(primaryColorSensor);
    int secondaryBlackMeasured = setBlackForSensor(secondaryColorSensor);
    openBlocker();
    stringDisk();
    BeltMotor->run(FORWARD);
    waitTime(1000);
    BeltMotor->run(RELEASE);
  //have we done valid readings
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
  // make an average and set it
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
