

int stringDisk(){  
  StringerMotor->run(BACKWARD);
  Serial.println("Opening...");
  delay(200);
  while (true) {
    int readVal = digitalRead(stringerPositionSensor);
    if (readVal == LOW) {
      break;
    }  
  }
  while (true) {
    int readVal = digitalRead(stringerPositionSensor);
    if (readVal == HIGH) {
      StringerMotor->run(RELEASE);
      Serial.println("Opened Stringer");
      break;
    }
  }
    delay(2000);
    Serial.println("Closing...");
    StringerMotor->run(FORWARD);
    delay(200);
    while (true) {
    int readVal = digitalRead(stringerPositionSensor);
    if (readVal == LOW) {
      break;
    }  
  }
  while (true) {
    int readVal = digitalRead(stringerPositionSensor);
    if (readVal == HIGH) {
      StringerMotor->run(RELEASE);
      Serial.println("Closed Stringer");
      break;
    }
  }
  secondaryMotionFlagged = false;
  return CONFIRM_STRING_DISK;
}
