using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pusher : MonoBehaviour
{
    // The communicator
    public GameObject communicator;

    // Speed of pusher
    public float speed = 1.0f;

    // Key
    public string key;

    // End and start position
    public Vector3 start;
    public Vector3 end;

    // Current and target position
    private Vector3 current;
    private Vector3 target;

    // Time when movement starts
    private float startTime;

    // Whether the pusher is extended
    private PusherState state;

    // Whether the pusher should do a push
    private bool doPush = false;

    // Total distance between the markers.
    private float distanceTotal;

    // Start is called before the first frame update
    void Start()
    {
        state = PusherState.Retracted;

        distanceTotal = Vector3.Distance(start, end);

        current = start;
        target = start;
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(key))
        {
            Push();
        }


        if (state == PusherState.Extending || state == PusherState.Retracting)
        {
            // Calculate the fraction of current distance over total distance
            float distance = (Time.time - startTime) * speed;
            float distanceFraction = distance / distanceTotal;

            // Put the pusher on fraction of the distance
            transform.position = Vector3.Lerp(current, target, distanceFraction);

            // If the pusher reached its total distance
            if (distance >= distanceTotal)
            {
                // Update state
                if (state == PusherState.Extending)
                {
                    state = PusherState.Extended;

                    if (doPush)
                    {
                        if (name == "Stringer")
                        {
                            GameObject.Find("Funnel").GetComponent<Funnel>().Next();
                        }

                        Retract();
                    }
                    else
                    {
                        ConfirmState();
                    }
                }
                else
                {
                    state = PusherState.Retracted;

                    if (doPush)
                    {
                        doPush = false;
                        ConfirmPush();
                    }
                    else
                    {
                        ConfirmState();
                    }
                }
            }
        }
    }

    // Extend
    public void Extend()
    {
        state = PusherState.Extending;
        startTime = Time.time;
        current = transform.position;
        target = end;
    }

    // Retract
    public void Retract()
    {
        state = PusherState.Retracting;
        startTime = Time.time;
        current = transform.position;
        target = start;
    }

    // Push
    public void Push()
    {
        doPush = true;
        Extend();
    }

    // Confirm push
    private void ConfirmState()
    {
        // Communicate push
        communicator.GetComponent<Communicator>().Communicate("Confirm " + name + " " + state);
    }

    // Confirm current state
    private void ConfirmPush()
    {
        // Communicate state
        if (name != "Stringer")
        {
            communicator.GetComponent<Communicator>().Communicate("Confirm " + name + " Pushed");
        }
    }
}
