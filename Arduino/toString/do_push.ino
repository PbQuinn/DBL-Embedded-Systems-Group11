

int doPush() {
  //turn of the belt motor to save power
  BeltMotor->run(RELEASE);
  BlockerMotor->run(FORWARD);
  waitTime(2000);
  while (true) {
    if (consistentlyPushed(pusherSensor)) {
      wait till we push consistantly
      BlockerMotor->run(RELEASE);
      break;
    }
    
  }
  BeltMotor->run(FORWARD);
  waitTime(2000);
  return CONFIRM_DO_PUSH;
}

bool consistentlyPushed(int sensor) {
  // is the sensor accurate in its readings
  for (int i = 0; i < 10; i++) {
    int readVal = digitalRead(sensor);
    if (readVal == LOW) {
      return false;
    }
    waitTime(5);
  }

  return true;
}
