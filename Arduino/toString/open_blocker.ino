
int openBlocker(){  
  BeltMotor->run(RELEASE);
  BlockerMotor->run(BACKWARD);
  while (true) {
    waitTime(5);
    int readVal = digitalRead(blockerBackSensor);
    if (readVal == LOW) {
      break;
    }  
  }
  BlockerMotor->run(RELEASE);
 
  
  BeltMotor->run(FORWARD);
  //we can now start detecting motion again
  primaryMotionFlagged = false;
  return CONFIRM_OPEN_GATE;
}
