
int exitSetup(){

  if(rangemaker(primary_black, primary_white, primary_ranges) && rangemaker(secondary_black, secondary_white, secondary_ranges)){
    BeltMotor->run(FORWARD);
    setBeltRange();
    state = 1;
    return CONFIRM_EXIT_SETUP;
  } else {
    return SETUP_FAIL;
  }
}


void setBeltRange(){
  float readings[sampleSize];
  float counterValue = 0;
  
  for(int i = 0; i < sampleSize; i++){
    float readValue = analogRead(primaryMotionSensor);
    counterValue += readValue;
    readings[i] = readValue;
    delay(100);
  }

  float averageValue = counterValue/sampleSize;

  belt_range[0] = averageValue - 150;
  belt_range[1] = averageValue + 100;

  Serial.print("Belt assigned: " );
  Serial.print(averageValue);

}
