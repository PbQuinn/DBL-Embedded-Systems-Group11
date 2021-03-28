
int openBlocker(){  
  BeltMotor->run(RELEASE);
  BlockerMotor->run(BACKWARD);
  while (true) {
    int readVal = digitalRead(blockerBackSensor);
    if (readVal == LOW) {
      break;
    }  
  }
  BlockerMotor->run(RELEASE);
 
  
  BeltMotor->run(FORWARD);
  return CONFIRM_OPEN_GATE;
}
