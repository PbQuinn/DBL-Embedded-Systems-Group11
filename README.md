# DBL-Embedded-Systems-Group11 - 'toString()'
This project consists of the control software for the robot made by group 11 as well as a unity simulation. The control software is meant to be ran on an RPI, together with either an Arduino connected to the toString robot, or the aforementioned unity simulation.

## The RPI
The control software running on the RPI was written in Python using object oriented programming. The structure of the code can be seen in the class diagram below.
![image](https://user-images.githubusercontent.com/64268431/112851376-36e95200-90ab-11eb-8662-bb7d93d5f2a2.png)
The code running on the RPI is responsible for receiving and sending messages to the Arduino that controls the sensors and motors in the robot, or the Simulation. On top of this, it also needs to interact with the protocol and keep track of what color the next disk to be stringed should be. All these tasks have been divided over multiple classes.

The `Communicator` is responsible for sending and receiving messages to the Arduino or simulation. Since the interface of the Arduino is different from the interface of the simulation, this class was made abstract.
The messages received by the `Communicator` then get passed on to an instance of the `Processor` class. The `Processor` will process the input and return the corresponding outputs. These outputs will then be communicated back to the Arduino, or Simulation by the `Communicator`.

The `Processor` is also responsible for deciding whether a disk should be picked up or not. This decision is made based on whether the protocol permits it, and the state of the string. To check for permission with the protocol, the `Processor` has an instance of `ProtocolHandler`, which is responsible for interacting with the protocol. The `Processor` also has an instance of `StringHandler`, which keeps track of the state of the string.

Finally, the `Processor` has an instance of `ExpectationHandler`. Every time the `Processor` sends output to the `Communicator` to which a response will be expected, an `Expectation` for that response will be added to the `ExpectationHander`. Each `Expectation` has a variable in which it keeps track of how many times it can be pinged before it expires. Once this happens, an error with a descriptive message is raised by the `ExpectationHander`. This error is then caught by the `Processor` which will convey the message to the user by printing it to the console.

## The Arduino
Text about Arduino code here

## The Simulation
Text about the code related to the Simulation here
