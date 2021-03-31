
int exitSetup(){

  if(rangemaker(primary_black, primary_white, primary_ranges) && rangemaker(secondary_black, secondary_white, secondary_ranges)){
    BeltMotor->run(FORWARD);
    setBeltRange();
    setFunnelRange();
    state = 1;
    Serial.print(primary_black);
    Serial.print(", ");
    Serial.println(primary_white);
    return CONFIRM_EXIT_SETUP;
  } else {
    return SETUP_FAIL;
  }
}


void setBeltRange(){
  float counterValue = 0;
  
  for(int i = 0; i < sampleSize; i++){
    float readValue = analogRead(primaryMotionSensor);
    counterValue += readValue;
    waitTime(100);
  }

  float averageValue = counterValue/sampleSize;

  belt_range[0] = averageValue - 150;
  belt_range[1] = averageValue + 100;
}



void setFunnelRange(){
  float counterValue = 0;
  
  for(int i = 0; i < sampleSize; i++){
    float readValue = analogRead(secondaryColorSensor);
    counterValue += readValue;
    waitTime(100);
  }

  float averageValue = counterValue/sampleSize;

  funnel_range[0] = averageValue - 10;
  funnel_range[1] = averageValue + 10;
}
