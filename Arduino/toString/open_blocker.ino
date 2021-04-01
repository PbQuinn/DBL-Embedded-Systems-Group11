
int openBlocker(){  
  // turn of the motor for the belt to save power
  BeltMotor->run(RELEASE);
  BlockerMotor->run(BACKWARD);
  //push until we have opend
  while (true) {
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
