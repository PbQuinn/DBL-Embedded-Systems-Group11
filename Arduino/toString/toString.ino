//====COMMAND NUMBERS====
//Gate control:
const int CLOSE_GATE = 10;
const int OPEN_GATE = 50;
const int DO_PUSH = 30;
//Sensor request:
const int GET_COLOR = 20;
const int AFFIRM_DISK = 40;
//Motor control:
const int STRING_DISK = 60;
//Program state control:
const int PING = 100;
//Callibration control:
const int SET_WHITE = 200;
const int SET_BLACK = 202;

//====RESPONSE NUMBERS====
//Action control:
const int NOTIFY_DISK_PRESENCE = 1;
const int CONFIRM_CLOSE_GATE = 11;
const int CONFIRM_OPEN_GATE = 51;
const int CONFIRM_DO_PUSH = 31;
const int CONFIRM_STRING_DISK = 61;
//Program state messages:
const int UNEXPECTED_ERROR = -1;
const int PONG = 101;
const int CONFIRM_SET_WHITE = 201;
const int CONFIRM_SET_BLACK = 203;
//For sensor requests:
const int WHITE = 21;
const int BLACK = 22;
const int NEITHER = 23;

void setup() {
  Serial.begin(9600);
  Serial.println("Successfully started IO hub");
}

//Communicate to the RPI that we're still operational.
void check(int issuedCommand) {
  switch (issuedCommand) {
    case PING:
      Serial.println(PONG);
      // do some action
      delay(100);
      break;

    case SET_WHITE:
      Serial.println(CONFIRM_SET_WHITE);
      // do some action
      delay(100);
      break;

    case SET_BLACK:
      Serial.println(CONFIRM_SET_BLACK);
      // do some action
      delay(100);
      break;

    case CLOSE_GATE:
      Serial.println(CONFIRM_CLOSE_GATE);
      // do some action
      delay(100);
      break;

    case OPEN_GATE:
      Serial.println(CONFIRM_OPEN_GATE);
      // do some action
      delay(100);
      break;

    case DO_PUSH:
      Serial.println(CONFIRM_DO_PUSH);
      // do some action
      delay(100);
      break;

    case GET_COLOR:
      Serial.println("SOME VALUE");
      // do some action
      delay(100);
      break;

    case AFFIRM_DISK:
      Serial.println("I THINK, I YES");
      // do some action
      delay(100);
      break;

    case STRING_DISK:
      Serial.println(CONFIRM_STRING_DISK);
      // do some action
      delay(100);
      break;

    default:
      // we get something we did not understand
      // we should normally send an error message but for now we just ignore it
      Serial.print("unknown action! ");
      Serial.println(UNEXPECTED_ERROR);
      break;
  }
}

int value = 0;

void loop() {

//This if-statement is responsible for taking input
//from the serial monitor. The call to check() is what truly
//handles the command.

//Check if there is a command waiting for me
  if (Serial.available() > 0) {
    char nextChar = Serial.read();
    //Have I finished reading this command?
    if (nextChar == '\n') {
      Serial.print("SENT: ");
      Serial.println(value);
      Serial.print("RECEIVED: ");
      //Send the command
      check(value);
      value = 0;
      //Otherwise, continue constructing the command issued
    } else {
      int intValue = nextChar - '0';
      value = 10 * value;
      value = value + intValue;
    }
  }




  // TODO: Implement scanning to write to "diskFound"
  bool diskFound = false;
  if (diskFound) {
    Serial.write(NOTIFY_DISK_PRESENCE);
  }
}
