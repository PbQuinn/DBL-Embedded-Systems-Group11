
int openBlocker(){  
  BeltMotor->run(RELEASE);
  BlockerMotor->run(BACKWARD);
  while (true) {
    int readVal = digitalRead(pusherSensor);
    if (readVal == LOW) {
      break;
    }  
  }
  while (true) {
    int readVal = digitalRead(blockerPositionSensor);
    if (readVal == HIGH) {
      break;
    }  
  }
  
  Serial.println("Opening blocker...");
  while (true) {
    int readVal = digitalRead(blockerPositionSensor);
    if (readVal == LOW) {
      BlockerMotor->run(RELEASE);
      Serial.println("Opened Blocker");
      break;
    }
  }
  
  BeltMotor->run(FORWARD);
  return CONFIRM_OPEN_GATE;
}
