

void waitTime(int milliseconds){

  int startTime = millis();
  int currentTime = millis();
  while(currentTime - startTime < milliseconds){
    checkInterrupt();
    currentTime = millis();
  }
}
