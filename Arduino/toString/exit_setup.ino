
int exitSetup(){

  if(setNeither() > 0 && rangemaker(primary_neither, primary_black, primary_white, primary_ranges) && rangemaker(secondary_neither, secondary_black, secondary_white, secondary_ranges)){
    BeltMotor->run(FORWARD);
    state = 1;
    return CONFIRM_EXIT_SETUP;
  } else {
    return SETUP_FAIL;
  }
}

int setNeither(){
  int primaryNeitherMeasured = setNeitherForSensor(primaryColorSensor);
  int secondaryNeitherMeasured = setNeitherForSensor(secondaryColorSensor);
  
  if(primaryNeitherMeasured > 0 && secondaryNeitherMeasured > 0){
    primary_neither = primaryNeitherMeasured;
    secondary_neither = secondaryNeitherMeasured;
    return 1;
  } else {
    return SETUP_FAIL;
  }
}

int setNeitherForSensor(int sensorPin){
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
  Serial.print("No outliers detected, neither assigned: " );
  Serial.print(averageValue);
  Serial.print(" for pin ");
  Serial.println(sensorPin);
  
  return averageValue;
}
