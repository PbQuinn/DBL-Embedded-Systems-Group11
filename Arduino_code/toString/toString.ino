//define a timer
//define a standard response
unsigned long timer = 0;
int connecter = 1;


void setup() {
  Serial.begin(9600);
}

//Communicate to the RPI that we're still operational.
void check(){
  if (Serial.available() > 0) {
    char message = Serial.read();
    switch (message){
      case '4':
        Serial.write(23);
        // do some action
        delay(100);
        break;
      default:
        // we get something we did not understand
        // we should normally send an error message but for now we just ignore it 
        Serial.println("unknown action!");
        break;
    }
  }
}

void loop() {
  if(millis() - 1000 > timer){
    timer = millis();
    Serial.write(connecter);
  }
  check();
}
