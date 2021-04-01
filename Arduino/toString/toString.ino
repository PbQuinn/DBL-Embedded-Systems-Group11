
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
             PONG, SET_ERROR_STATE, EXIT_ERROR_STATE, SET_WHITE, SET_BLACK, EXIT_SETUP
            };

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
const int UNEXPECTED_ERROR = 254;
const int ILLEGAL_COMMAND = 253;
const int UNKNOWN_COMMAND = 252;
const int BUFFER_FULL = 251;
const int SETUP_FAIL = 250;
const int PING = 101;
const int ERROR_PING = 103;
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
   0: the initialisation state
   1: the working state
   2: the error state
*/
int state = 0;
//A boolean to check whether we missed an expected response
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
int funnel_range[2];


//FLAGS
bool flagRead;
bool primaryMotionFlagged;
bool secondaryMotionFlagged;


void setup() {
  Serial.begin(9600);
  Timer1.initialize(1000000);
  Timer1.attachInterrupt( interrupt );

  pinMode(stringerPositionSensor, INPUT);
  pinMode(blockerBackSensor, INPUT);
  pinMode(pusherSensor, INPUT);


  AFMS.begin();
  StringerMotor->setSpeed(200);
  BlockerMotor->setSpeed(250);
  BeltMotor->setSpeed(200);
}



int getMessage() {
  int value = 0;
  while (true) {
    if (Serial.available() > 0) {
      char nextChar = Serial.read();

      //Have I finished reading this command?
      if (nextChar == '\n') {
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
  //This if-statement is responsible for taking input
  //from the serial monitor. The call to check() is what truly
  //handles the command.
  while (Serial.available() > 0) {
    int message = getMessage();
    //first we need to check if the command is pong or entering the error state.
    //in those cases we need to handle them immediatly else we put the request in the que
    if (message == PONG) {
      expected = false;
    } else if (message == SET_ERROR_STATE) {
      if (state != 2) {
        enterErrorState();
      }
    } else if (message == EXIT_ERROR_STATE && state == 2) {
      state = 1;
      Serial.write(CONFIRM_EXIT_ERROR_STATE);
    } else {
      if ((writep + 1) % 10 == readp) {
        Serial.write(BUFFER_FULL);
      } else {
        que[writep] = message;
        writep = (writep + 1) % 10;
      }
    }
  }

  if (expected && state != 2) {
    //enterErrorState();
  }

  // if we are working we should check the connection
  if (state == 1) {
    Serial.write(PING);
    expected = true;
  }

  flagRead = false;
}

void interrupt() {
  flagRead = true;
}

//check the use cases
void check(int issuedCommand) {
  switch (issuedCommand) {

    case SET_WHITE:
      Serial.write(setWhite());
      // do some action
      waitTime(100);
      break;

    case SET_BLACK:
      Serial.write(setBlack());
      // do some action
      waitTime(100);
      break;

    case EXIT_SETUP:
      Serial.write(exitSetup());
      waitTime(100);
      Serial.write(123);
      Serial.write(primary_ranges[0]);
      Serial.write(123);
      Serial.write(primary_ranges[1]);
      Serial.write(123);
      Serial.write(primary_ranges[2]);
      Serial.write(123);
      Serial.write(primary_ranges[3]);
      break;


    case EXIT_ERROR_STATE:
      BeltMotor->run(FORWARD);
      state = 1;

      Serial.write(CONFIRM_EXIT_ERROR_STATE);
      waitTime(100);
      break;

    case CLOSE_BLOCKER:
      Serial.write(closeBlocker());
      // do some action
      waitTime(100);
      break;

    case OPEN_BLOCKER:
      Serial.write(openBlocker());
      // do some action
      waitTime(100);
      break;

    case DO_PUSH:
      Serial.write(doPush());
      // do some action
      waitTime(100);
      break;

    case GET_COLOR:
      Serial.write(getColor(primaryColorSensor, primary_ranges));
      // do some action
      waitTime(100);
      break;

    case AFFIRM_DISK:
    // control software reasons about sensor number by looking at values in range 41-43 instead of 21-23
      Serial.write(getColor(secondaryColorSensor, secondary_ranges)+20);
      // do some action
      waitTime(100);
      break;

    case STRING_DISK:
      int stringReturn = stringDisk();
      if (stringReturn > 0){
        Serial.write(stringReturn);
      }
      // do some action
      waitTime(100);
      break;


    default:
      // By the state check this default should not be reachable
      Serial.write(UNEXPECTED_ERROR);
      break;
  }
}

boolean in(int number, int commands[], int commandsLength) {
  for (int i = 0; i < commandsLength; i++) {
    if (number == commands[i]) {
      return true;
    }
  }
  return false;
}

boolean stateCheck(int message) {
  if (state == 0) {
    if (in(message, setupmessages, setupmessagesLength)) {
      return true;
    } else if (in(message, all, allLength)) {
      Serial.write(ILLEGAL_COMMAND);
      return false;
    } else {
      Serial.write(UNKNOWN_COMMAND);
      return false;
    }
  } else if (state == 1) {
    if (in(message, workmessages, workmessagesLength)) {
      return true;
    } else if (in(message, all, allLength)) {
      Serial.write(ILLEGAL_COMMAND);
      return false;
    } else {
      Serial.write(UNKNOWN_COMMAND);
      return false;
    }
  } else if (state == 2) {
    if (in(message, errormessages, errormessagesLength)) {
      return true;
    } else if (in(message, all, allLength)) {
      Serial.write(ILLEGAL_COMMAND);
      return false;
    } else {
      Serial.write(UNKNOWN_COMMAND);
      return false;
    }
  }
}

void enterErrorState() {
  expected = false;
  state = 2;
  //clear the buffer
  while (Serial.available() > 0) {
    int imGonnaTrashYou = Serial.read();
  }
  openBlocker();
  readp = writep;
  Serial.write(ERROR_PING);
}


void checkInterrupt() {
  if (flagRead) {
    messages();
  }
}

int lastPrimaryMotion = millis();
int lastSecondaryMotion = millis();
int flagExpire = 5000;

void loop() {
  waitTime(10);
  //Check if there is a command to process
  if (writep != readp) {
    int message = que[readp];
    readp = (readp + 1) % 10;
    if (stateCheck(message)) {
      check(message);
    }
  }
  //Serial.print(analogRead(primaryColorSensor));  Serial.print("   ");  Serial.print(analogRead(secondaryColorSensor));  Serial.print("   ");  Serial.print(analogRead(A2));  Serial.print("   ");  Serial.print(analogRead(A3));  Serial.print("   ");  Serial.print(analogRead(A4));  Serial.print("   ");  Serial.print(analogRead(A5));  Serial.println("   ");
  
  if (state == 1) {
    //If the flag for primary motion has not been lowered for the past 5 seconds.
    int timeSinceLastPrimaryMotion = millis() - lastPrimaryMotion;
    int timeSinceLastSecondaryMotion = millis() - lastSecondaryMotion;
    
    if (primaryMotionFlagged && timeSinceLastPrimaryMotion > flagExpire){
      primaryMotionFlagged = false;
    }

    if (secondaryMotionFlagged && timeSinceLastSecondaryMotion > flagExpire){
      secondaryMotionFlagged = false;
    }
    
    if (checkPrimaryMotion() && !primaryMotionFlagged) {
      lastPrimaryMotion = millis();
      primaryMotionFlagged = true;
      Serial.write(NOTIFY_DISK_PRESENCE);
    }

    if (checkSecondaryMotion() && !secondaryMotionFlagged) {
      lastSecondaryMotion = millis();
      secondaryMotionFlagged = true;
      Serial.write(NOTIFY_DISK_ARRIVAL);
    }
  }
}
