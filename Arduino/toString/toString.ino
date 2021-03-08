//====COMMAND NUMBERS====
//Gate control:
const int CLOSE_BLOCKER = 10;
const int OPEN_BLOCKER = 50;
const int DO_PUSH = 30;
//Sensor request:
const int GET_COLOR = 20;
const int AFFIRM_DISK = 40;
//Motor control:
const int STRING_DISK = 60;
//Program state control:
const int PING = 100;
const int SET_ERROR_STATE = 102;
const int EXIT_ERRO_STATE = 104;
const int GET_ERROR_STATE_INFO = 106;
//Callibration control:
const int SET_WHITE = 200;
const int SET_BLACK = 202;
const int EXIT_SETUP = 204

//====RESPONSE NUMBERS====
//Action control:
const int NOTIFY_DISK_PRESENCE = 1;
const int CONFIRM_CLOSE_GATE = 11;
const int CONFIRM_OPEN_GATE = 51;
const int CONFIRM_DO_PUSH = 31;
const int CONFIRM_STRING_DISK = 61;
//Program state messages:
const int UNEXPECTED_ERROR = -1;
const int ILLEGAL_COMMAND = -2;
const int UNKNOWN_COMMAND = -3;
const int PONG = 101;
const int ERRONG_PING = 103;
const int CONFIRM_EXIT_ERROR_STATE = 105;
const int GET_ERROR_STATE_INFO = 106;
const int START_MESSAGE = 107;
const int END_MESSGE = 108;
const int CONFIRM_SET_WHITE = 201;
const int CONFIRM_SET_BLACK = 203;
const int CONFIRM_EXIT_SETUP = 205;
//For sensor requests:
const int WHITE = 21;
const int BLACK = 22;
const int NEITHER = 23;

void setup() {
  Serial.begin(9600);
  // A timer to check if we are not disconnected
  unsigned long timer = 0;
  /* The current state we are in:
  * 0: the initialisation state 
  * 1: the working state
  * 2: the error state
  */
  int state = 0;
  //Serial.println("Successfully started IO hub");
}

//Communicate to the RPI that we're still operational.
void check(int issuedCommand) {
  switch (issuedCommand) {
    case PING:
      Serial.write(PONG)
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
    int message = Serial.read() - '0';
    check(value);
  }




  // TODO: Implement scanning to write to "diskFound"
  bool diskFound = false;
  if (diskFound) {
    Serial.write(NOTIFY_DISK_PRESENCE);
  }
}
