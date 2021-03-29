  
//a libary used for interupts
#include <TimerOne.h>
#include <Adafruit_MotorShield.h>

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
//Callibration control:
const int SET_WHITE = 200;
const int SET_BLACK = 202;
const int EXIT_SETUP = 204;

//working state possibilities
int workmessages[] = {CLOSE_BLOCKER, OPEN_BLOCKER, DO_PUSH, GET_COLOR, AFFIRM_DISK, STRING_DISK, PONG, SET_ERROR_STATE};
int errormessages[] = {EXIT_ERROR_STATE, PONG};
int setupmessages[] = {SET_WHITE, SET_BLACK, EXIT_SETUP, PONG};
int all[] = {CLOSE_BLOCKER, OPEN_BLOCKER, DO_PUSH, GET_COLOR, AFFIRM_DISK, STRING_DISK,
            PONG, SET_ERROR_STATE, EXIT_ERROR_STATE, SET_WHITE, SET_BLACK, EXIT_SETUP};

int workmessagesLength = 8;
int errormessagesLength = 2;
int setupmessagesLength = 4;
int allLength = 12;

//====RESPONSE NUMBERS====
//Action control:
const int NOTIFY_DISK_PRESENCE = 1;
const int NOTIFY_DISK_ARRIVAL = 2;
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
const int SETUP_FAIL = -5;
const int PING = 101;
const int ERRONG_PING = 103;
const int CONFIRM_EXIT_ERROR_STATE = 105;
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


Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *StringerMotor = AFMS.getMotor(3);
Adafruit_DCMotor *BlockerMotor = AFMS.getMotor(4);
Adafruit_DCMotor *BeltMotor = AFMS.getMotor(1);

int stringerPositionSensor = 6;
int blockerFrontSensor = 2;
int blockerBackSensor = 3;
int pusherSensor = 4;

int primaryColorSensor = A1;
int secondaryColorSensor = A0;
int tertiaryMotionSensor = A2;
int primaryMotionSensor = A3;

const int sampleSize = 10;
const int consistencyLimit = 50;


int primary_white;
int primary_black;

int secondary_white;
int secondary_black;

int primary_ranges[6];
int secondary_ranges[6];
int belt_range[2];

bool secondaryMotionFlagged;


void setup() {
  Serial.begin(9600);
  Serial.println("Successfully started IO hub");
  Timer1.initialize(100000); 
  Timer1.attachInterrupt( messages );
  
  pinMode(stringerPositionSensor, INPUT);
  pinMode(blockerBackSensor, INPUT);
  pinMode(pusherSensor, INPUT);

  
  AFMS.begin();
  StringerMotor->setSpeed(200);
  BlockerMotor->setSpeed(250);
  BeltMotor->setSpeed(200);
}


int getMessage(){
  int value = 0;
  while(true){
    if (Serial.available() > 0) {
    char nextChar = Serial.read();
    //Have I finished reading this command?
    if (nextChar == '\n') {
      Serial.print("SENT: ");
      Serial.println(value);
      Serial.print("RECEIVED: ");
      //Send the command
      return value;
      //Otherwise, continue constructing the command issued
    } else {
      int intValue = nextChar - '0';
      value = 10 * value;
      value = value + intValue;
    }
  }
  }
}

void messages() {
  //we need to check the message pool
  while (Serial.available() > 0) {
    Serial.println("doing serial stuff");
    int message = getMessage();
    //first we need to check if the command is pong or entering the error state.
    //in those cases we need to handle them immediatly else we put the request in the que
    if(message == PONG){
      expected = false;
    }else if(message == SET_ERROR_STATE){
      enterErrorState();
    }else{
      if(writep+ 1 == readp){
        Serial.println(BUFFER_FULL);
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
  // CAUTION: TURNED OFF TEMPORARILY!!!!
  if(state == 1 && false){
      Serial.println(PING);
      expected = true;
  }
}

void openGate(){
  Serial.write(CONFIRM_OPEN_GATE);
}


//check the use cases 
void check(int issuedCommand) {
  switch (issuedCommand) {
    case PING:
      Serial.println(PONG);
      break;

    case SET_WHITE:
      Serial.println(setWhite());
      // do some action
      delay(100);
      break;

    case SET_BLACK:    
      Serial.println(setBlack());
      // do some action
      delay(100);
      break;

    case EXIT_SETUP:
      Serial.println(exitSetup());
      delay(100);
      break;


    case EXIT_ERROR_STATE:

      state = 1;
    
      Serial.println(CONFIRM_EXIT_ERROR_STATE);
      delay(100);
      break;
    case CLOSE_BLOCKER:
      Serial.println(closeBlocker());
      // do some action
      delay(100);
      break;

    case OPEN_BLOCKER:
      Serial.println(openBlocker());
      // do some action
      delay(100);
      break;

    case DO_PUSH:
      Serial.println(doPush());
      // do some action
      delay(100);
      break;

    case GET_COLOR:
      Serial.println(getColor(primaryColorSensor, primary_ranges));
      // do some action
      delay(100);
      break;

    case AFFIRM_DISK:
      Serial.println("I THINK, I YES");
      // do some action
      delay(100);
      break;

    case STRING_DISK:
      Serial.println(stringDisk());
      // do some action
      delay(100);
      break;
      
      
    default:
      // By the state check this default should not be reachable
      Serial.write(UNEXPECTED_ERROR);
      break;
  }
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
  if(state == 0){
    if(in(message, setupmessages, setupmessagesLength)){
      return true;
    }else if(in(message, all, allLength)){
      Serial.println(ILLEGAL_COMMAND);
      return false;
    }else{
      Serial.println(UNKNOWN_COMMAND);
      return false;
    }
  }else if(state == 1){
    if(in(message, workmessages, workmessagesLength)){
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
      Serial.write(UNKNOWN_COMMAND);
      return false;
    }
  }
}

void enterErrorState(){
  state = 2;
  //clear the buffer
  openGate();
  readp = writep;
  while(state == 2){
    Serial.println(ERRONG_PING);
    delay(100);
  }

}


void loop() {
//Serial.print(analogRead(primaryColorSensor));  Serial.print("   ");  Serial.print(analogRead(secondaryColorSensor));  Serial.print("   ");  Serial.print(analogRead(A2));  Serial.print("   ");  Serial.print(analogRead(A3));  Serial.print("   ");  Serial.print(analogRead(A4));  Serial.print("   ");  Serial.print(analogRead(A5));  Serial.println("   ");
//Serial.println(digitalRead(blockerFrontSensor));
delay(10);
//Check if there is a command to process
  if(writep != readp){
    int message = que[readp];
    readp = (readp + 1) % 10;
    if(stateCheck(message)){
      check(message);
    }      
  }  




  // TODO: Implement scanning to write to "diskFound"
  if(state == 1){
    //Serial.print("Primary: ");
    //Serial.print(analogRead(primaryColorSensor));
    //Serial.print(",      Secondary: ");
    //Serial.println(analogRead(secondaryColorSensor));

      //Serial.println(analogRead(primaryMotionSensor));
      if (checkPrimaryMotion()){
        Serial.println("Yo");
        closeBlocker();
        delay(1500);
        if(getColor(primaryColorSensor, primary_ranges) == WHITE){
          doPush();
        }
        openBlocker();
        delay(1000);
      }
      
      if (checkSecondaryMotion() && !secondaryMotionFlagged) {
        secondaryMotionFlagged = true;
        Serial.println(NOTIFY_DISK_ARRIVAL);
        delay(1000);
        stringDisk();
       
      }
  }

}
