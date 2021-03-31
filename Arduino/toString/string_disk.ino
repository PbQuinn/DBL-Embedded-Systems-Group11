

int stringDisk(){  
  StringerMotor->run(BACKWARD);
  waitTime(200);
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
      break;
    }
  }
    waitTime(2000);
    StringerMotor->run(FORWARD);
    waitTime(200);
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
      break;
    }
  }
  secondaryMotionFlagged = false;
  return CONFIRM_STRING_DISK;
}
