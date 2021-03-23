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
const int SETUP_STATE = 0;
const int WORKING_STATE = 1;
const int ERROR_STATE = 2;
const int PING = 100;
const int SET_ERROR_STATE = 102;
const int EXIT_ERROR_STATE = 104;
const int GET_ERROR_STATE_INFO = 106;
//Callibration control:
const int SET_WHITE = 200;
const int SET_BLACK = 202;
const int EXIT_SETUP = 204;


//working state possibilities
int workmessages[] = {CLOSE_BLOCKER, OPEN_BLOCKER, DO_PUSH, GET_COLOR, AFFIRM_DISK, STRING_DISK, PING, SET_ERROR_STATE};
int errormessages[] = {EXIT_ERROR_STATE, GET_ERROR_STATE_INFO, PING};
int setupmessages[] = {SET_WHITE, SET_BLACK, EXIT_SETUP, PING};
int all[] = {CLOSE_BLOCKER, OPEN_BLOCKER, DO_PUSH, GET_COLOR, AFFIRM_DISK, STRING_DISK,
            PING, SET_ERROR_STATE,EXIT_ERROR_STATE, GET_ERROR_STATE_INFO, SET_WHITE, SET_BLACK, EXIT_SETUP};

//====RESPONSE NUMBERS====
//Action control:
const int NOTIFY_DISK_PRESENCE = 1;
const int CONFIRM_CLOSE_GATE = 11;
const int CONFIRM_OPEN_GATE = 51;
const int CONFIRM_DO_PUSH = 31;
const int CONFIRM_STRING_DISK = 61;
const int ERROR_STRING_DISK = 62;
//Program state messages:
const int UNEXPECTED_ERROR = -1;
const int ILLEGAL_COMMAND = -2;
const int UNKNOWN_COMMAND = -3;
const int PONG = 101;
const int ERRONG_PING = 103;
const int CONFIRM_EXIT_ERROR_STATE = 105;
const int START_MESSAGE = 107;
const int END_MESSGE = 108;
const int CONFIRM_SET_WHITE = 201;
const int CONFIRM_SET_BLACK = 203;
const int CONFIRM_EXIT_SETUP = 205;
//For sensor requests:
const int WHITE = 21;
const int BLACK = 22;
const int NEITHER = 23;
// How often should we recieve Ping messages + some time to avoid false positives in ms.
const int PING_TIME = 1500;
// A timer to check if we are not disconnected
unsigned long timer = 0;
/* The current state we are in:
 * 0: the initialisation state 
 * 1: the working state
 * 2: the error state
 */
int state = 0;
<<<<<<< Updated upstream
=======
//A boolean to check wheter we missed an expected response
boolean expected = false;
//make a circular buffer
int que[10];
int readp = 0;
int writep = 0;


Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *StringerMotor = AFMS.getMotor(3);
Adafruit_DCMotor *BlockerMotor = AFMS.getMotor(4);


int stringerPositionSensor = 6;
int blockerPositionSensor = 3;
int pusherSensor = 4;
int primaryColorSensor = A0;
int secondaryColorSensor = A1;

const int sampleSize = 10;
const int consistencyLimit = 50;


int primary_white;
int primary_black;
int primary_neither;

int secondary_white;
int secondary_black;
int secondary_neither;
>>>>>>> Stashed changes


void setup() {
  Serial.begin(9600);
  Serial.println("Successfully started IO hub");
}

//Communicate to the RPI that we're still operational.
void check(int issuedCommand) {
  switch (issuedCommand) {
    case PING:
      Serial.println(PONG);
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

    case EXIT_SETUP:
      state = WORKING_STATE;
      Serial.println(CONFIRM_EXIT_SETUP);
      delay(100);
      break;
      
    case CLOSE_BLOCKER:
      Serial.println(CONFIRM_CLOSE_GATE);
      // do some action
      delay(100);
      break;

    case OPEN_BLOCKER:
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
      Serial.println("Stringing disk...");
      delay(1000);
      Serial.println(CONFIRM_STRING_DISK);
      // do some action
      delay(100);
      break;

    default:
      // By the state check this default should not be reachable
      Serial.println(UNEXPECTED_ERROR);
      break;
  }
  Serial.println("");
}

boolean in(int number, int commands[], int commandsLength){
  for(int i = 0; i < commandsLength; i++){
    if(number == commands[i]){
      return true;
    }
  }
  return false;    
}

boolean stateCheck(int message) {

  int setupmessagesLength = sizeof(setupmessages) / sizeof(setupmessages[0]);
  int workmessagesLength = sizeof(workmessages) / sizeof(workmessages[0]);
  int errormessagesLength = sizeof(errormessages) / sizeof(errormessages[0]);
  int allLength = sizeof(all) / sizeof(all[0]); 
  
  if(state == 0){
    if(in(message,setupmessages, setupmessagesLength)){
      return true;
    }else if(in(message, all, allLength)){
      Serial.println(ILLEGAL_COMMAND);
      return false;
    }else{
      Serial.println(UNKNOWN_COMMAND);
      return false;
    }
  }else if(state == 1){
    if(in(message,workmessages, workmessagesLength)){
      return true;
    }else if(in(message, all, allLength)){
      Serial.println(ILLEGAL_COMMAND);
      return false;
    }else{
      Serial.println(UNKNOWN_COMMAND);
      return false;
    }
  }else if(state == 2){
    if(in(message, errormessages, errormessagesLength)){
      return true;
    }else if(in(message, all, allLength)){
      Serial.println(ILLEGAL_COMMAND);
      return false;
    }else{
      Serial.println(UNKNOWN_COMMAND);
      return false;
    }
  }
}

void enterErrorState(){
  
}



int value = 0;

void loop() {

//This if-statement is responsible for taking input
//from the serial monitor. The call to check() is what truly
//handles the command.

//Check if there is a command waiting for me


//  if (Serial.available() > 0) {
//    int message = Serial.read() - '0';
//
//    //first we need to check if the command is valid in the current state if so check it
//    if(stateCheck(message)){
//      check(message);
//    }
//  }


if (Serial.available() > 0) {
    char nextChar = Serial.read();
    //Have I finished reading this command?
    if (nextChar == '\n') {
      Serial.print("SENT: ");
      Serial.println(value);
      Serial.print("RECEIVED: ");
      //Send the command
      if(stateCheck(value)){
        check(value);
      }
      value = 0;
      //Otherwise, continue constructing the command issued
    } else {
      int intValue = nextChar - '0';
      value = 10 * value;
      value = value + intValue;
    }
  }


  // if we are working we should check the connection
  // any further working state specific actions should also be placed here
//  if(state == WORKING_STATE){
//    if(millis() - PING_TIME > timer){
//      enterErrorState();
//    }
//  }


  // TODO: Implement scanning to write to "diskFound"
  bool diskFound = false;
  if (diskFound) {
    Serial.println(NOTIFY_DISK_PRESENCE);
  }
}
