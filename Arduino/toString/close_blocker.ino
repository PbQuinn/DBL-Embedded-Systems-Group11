
int closeBlocker(){  
  BeltMotor->run(RELEASE);
  BlockerMotor->run(FORWARD);
  while (true) {
    int readVal = digitalRead(blockerFrontSensor);
    if (readVal == HIGH) {
      break;
    }  
  }
  BlockerMotor->run(RELEASE);
  
  BeltMotor->run(FORWARD);
  return CONFIRM_CLOSE_GATE;
}
