

int stringDisk(){  
  //open the stringer untill we have sensed he has opend
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
  // wait for the disk to fall and start stringing the disk
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
  // we have stringed the disk we do not have to do it again we also signal the RPI
  secondaryMotionFlagged = false;
  return CONFIRM_STRING_DISK;
}
