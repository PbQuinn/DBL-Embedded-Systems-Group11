

int doPush(){  
  BeltMotor->run(RELEASE);
  BlockerMotor->run(FORWARD);
  delay(100);
  while (true) {
    int readVal = digitalRead(pusherSensor);
    if (readVal == HIGH) {
      BlockerMotor->run(RELEASE);
      break;
    }  
  } 
  BeltMotor->run(FORWARD);

  return CONFIRM_DO_PUSH;
}
