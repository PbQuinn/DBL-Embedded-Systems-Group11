

void waitTime(int milliseconds){
  //make a timer we still need to check if we are interupted so we read the messages.
  int startTime = millis();
  int currentTime = millis();
  while(currentTime - startTime < milliseconds){
    checkInterrupt();
    currentTime = millis();
  }
}
