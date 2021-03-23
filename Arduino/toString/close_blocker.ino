

int closeBlocker(){  
  BeltMotor->run(RELEASE);
  BlockerMotor->run(FORWARD);
  delay(300);
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
  return CONFIRM_CLOSE_GATE;
}
