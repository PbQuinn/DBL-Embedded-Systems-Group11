
int closeBlocker(){  
  //turn of the belt motor to save power
  BeltMotor->run(RELEASE);
  BlockerMotor->run(FORWARD);
  while (true) {
    //run while we are not blocking
    int readVal = digitalRead(blockerFrontSensor);
    if (readVal == HIGH) {
      break;
    }  
  }
  BlockerMotor->run(RELEASE);
  
  BeltMotor->run(FORWARD);
  return CONFIRM_CLOSE_GATE;
}
