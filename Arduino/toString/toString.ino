//a libary used for interupts
#include <TimerOne.h>

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
const int PONG = 100;
const int SET_ERROR_STATE = 102;
const int EXIT_ERROR_STATE = 104;
const int GET_ERROR_STATE_INFO = 106;
//Callibration control:
const int SET_WHITE = 200;
const int SET_BLACK = 202;
const int EXIT_SETUP = 204;

//working state possibilities
int workmessages[] = {CLOSE_BLOCKER, OPEN_BLOCKER, DO_PUSH, GET_COLOR, AFFIRM_DISK, STRING_DISK, PONG, SET_ERROR_STATE};
int errormessages[] = {EXIT_ERROR_STATE, GET_ERROR_STATE_INFO, PONG};
int setupmessages[] = {SET_WHITE, SET_BLACK, EXIT_SETUP, PONG};
int all[] = {CLOSE_BLOCKER, OPEN_BLOCKER, DO_PUSH, GET_COLOR, AFFIRM_DISK, STRING_DISK,
            PONG, SET_ERROR_STATE,EXIT_ERROR_STATE, GET_ERROR_STATE_INFO, SET_WHITE, SET_BLACK, EXIT_SETUP};

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
const int BUFFER_FULL = -4;
const int PING = 101;
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

// A timer to check if we are not disconnected
unsigned long timer = 0;
/* The current state we are in:
 * 0: the initialisation state 
 * 1: the working state
 * 2: the error state
 */
int state = 0;
//A boolean to check wheter we missed an expected response
boolean expected = false;
//make a circular buffer
int que[10];
int readp = 0;
int writep = 0;


void setup() {
  Serial.begin(9600);
  //Serial.println("Successfully started IO hub");
  Timer1.initialize(100000); 
  Timer1.attachInterrupt( messages );
}



void messages() {
  //we need to check the message pool
  //This if-statement is responsible for taking input
  //from the serial monitor. The call to check() is what truly
  //handles the command.
  while (Serial.available() > 0) {
    int message = Serial.read() - '0';
    //first we need to check if the command is pong or entering the error state.
    //in those cases we need to handle them immediatly else we put the request in the que
    if(message == PONG){
      expected = false;
    }else if(message == SET_ERROR_STATE){
      enterErrorState();
    }else if(message == EXIT_ERROR_STATE && state ==2){
      state = 1;
      Serial.write(CONFIRM_EXIT_ERROR_STATE);
    }else{
      if((writep + 1) % 10== readp){
        Serial.write(BUFFER_FULL);
      }else{
        que[writep] = message;
        writep = (writep + 1) % 10;
      }      
    }     
  }

  if(expected){
    enterErrorState();
  }
  
  // if we are working we should check the connection
  if(state == 1){
      Serial.write(PING);
      expected = true;
  }
}

void openGate(){
  Serial.write(CONFIRM_OPEN_GATE);
}


//check the use cases 
void check(int issuedCommand) {
  switch (issuedCommand) {
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
      state = 1;
      Serial.println(CONFIRM_EXIT_SETUP);

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
      Serial.println(CONFIRM_STRING_DISK);
      // do some action
      delay(100);
      break;

    default:
      // By the state check this default should not be reachable
      Serial.write(UNEXPECTED_ERROR);
      break;
  }
}

boolean in(int number, int commands[]){
  for(int i = 0; i < sizeof(commands) / sizeof(commands[0]); i++){
    if(number == commands[i]){
      return true;
    }
  }
  return false;    
}

boolean stateCheck(int message) {
  if(state == 0){
    if(in(message,setupmessages)){
      return true;
    }else if(in(message,all)){
      Serial.write(ILLEGAL_COMMAND);
      return false;
    }else{
      Serial.write(UNKNOWN_COMMAND);
      return false;
    }
  }else if(state == 1){
    if(in(message,workmessages)){
      return true;
    }else if(in(message,all)){
      Serial.write(ILLEGAL_COMMAND);
      return false;
    }else{
      Serial.write(UNKNOWN_COMMAND);
      return false;
    }
  }else if(state == 2){
    if(in(message,errormessages)){
      return true;
    }else if(in(message,all)){
      Serial.write(ILLEGAL_COMMAND);
      return false;
    }else{
      Serial.write(UNKNOWN_COMMAND);
      return false;
    }
  }
}

void enterErrorState(){
  state = 2;
  openGate();
  Serial.write(ERRONG_PING);
  //clear the buffer
  readp = writep;
  // clear the serial buffer
  while (Serial.available() > 0) {
    int message = Serial.read() - '0';
    if(message == EXIT_ERROR_STATE && state ==2){
      state = 1;
    }
  }
  while(state == 2){
    delay(100);
  }
}


void loop() {
//Check if there is a command to process
  if(writep != readp){
    int message = que[readp];
    readp = (readp + 1) % 10;
    if(stateCheck(message)){
      check(message);
    }      
  }  


  // TODO: Implement scanning to write to "diskFound"
  bool diskFound = false;
  if (diskFound) {
    Serial.write(NOTIFY_DISK_PRESENCE);
  }
}
