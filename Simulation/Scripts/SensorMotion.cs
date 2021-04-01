using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SensorMotion : MonoBehaviour
{
    // The communicator
    public GameObject communicator;

    // When something triggers the motion sensor
    private void OnTriggerEnter(Collider collider)
    {
        // Communicate motion
        communicator.GetComponent<Communicator>().Communicate(name);
    }
}
