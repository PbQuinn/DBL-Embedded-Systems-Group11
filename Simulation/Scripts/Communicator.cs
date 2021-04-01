using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using AsyncIO;
using NetMQ;
using NetMQ.Sockets;

public class Communicator : MonoBehaviour
{
    // Objects in simulation
    public GameObject pusher;
    public GameObject blocker;
    public GameObject stringer;
    public GameObject primaryColorSensor;
    public GameObject secondaryColorSensor;

    // Ping time
    public float pingTime;
    private float startTime;

    // Whether the simulation is in error mode
    private bool errorMode = false;

    // Start is called before the first frame update
    void Start()
    {
        startTime = Time.time;
    }

    // Update is called once per frame
    void Update()
    {
        if (Time.time - startTime >= pingTime)
        {
            startTime = Time.time;
            Communicate("Ping");
        }
    }

    // Send message to server, receive message from server, process message
    public void Communicate(string output)
    {
        ForceDotNet.Force();

        string input;

        using (RequestSocket client = new RequestSocket())
        {
            // Connect
            client.Connect("tcp://localhost:5555");

            // Send
            Send(client, output);

            // Receive
            input = Receive(client);
        }

        NetMQConfig.Cleanup();

        // Process
        Process(input);
    }

    // Sends message
    void Send(RequestSocket client, string output)
    {
        client.SendFrame(output);
        if (output != "Ping")
        {
            Debug.Log("Sent: " + output);
        }
    }

    // Receives and returns message
    string Receive(RequestSocket client)
    {
        bool gotInput;

        // If in error mode, set timespan to 100 ms, else to 1 s
        TimeSpan timeSpan;

        if (errorMode)
        {
            timeSpan = new TimeSpan(0, 0, 0, 0, 10);
        }
        else
        {
            timeSpan = new TimeSpan(0, 0, 0, 1);
        }

        // Try to receive message
        gotInput = client.TryReceiveFrameString(timeSpan, out string input);

        if (! gotInput)
        {
            input = "Nothing";
        }
        else if (errorMode)
        {
            errorMode = false;
        }

        if (input != "Pong" && input != "Nothing")
        {
            Debug.Log("Received: " + input);
        }
        return input;
    }

    // Processes received message
    void Process(string input)
    {
        string[] commands = input.Split(',');

        foreach (string command in commands)
        {
            switch (command)
            {
                case "Extend Blocker":
                    blocker.GetComponent<Pusher>().Extend();
                    break;
                case "Retract Blocker":
                    blocker.GetComponent<Pusher>().Retract();
                    break;
                case "Push Pusher":
                    pusher.GetComponent<Pusher>().Push();
                    break;
                case "Push Stringer":
                    stringer.GetComponent<Pusher>().Push();
                    break;
                case "Scan Primary Color":
                    primaryColorSensor.GetComponent<SensorColor>().Scan();
                    break;
                case "Scan Secondary Color":
                    secondaryColorSensor.GetComponent<SensorColor>().Scan();
                    break;
                case "Enter Error Mode":
                    blocker.GetComponent<Pusher>().Retract();
                    errorMode = true;
                    break;
            }
        }
    }
}
