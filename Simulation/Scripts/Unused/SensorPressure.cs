using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SensorPressure : MonoBehaviour
{
    // Current object on pressure sensor
    private GameObject currentObject;

    // Indicates if the mass of the current object has been measured
    private bool measured;

    // Start is called before the first frame update
    void Start()
    {
        currentObject = null;
        measured = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (currentObject != null && ! measured)
        {
            float mass = getMass();
            // Debug.Log(mass);

            if (mass > 900)
            {
                // Debug.Log("Pusher is extended!");
            }
        }
    }

    // Set colliding object as current object on the sensor
    private void OnTriggerEnter(Collider other)
    {
        measured = false;
        currentObject = other.gameObject;
    }

    // Remove colliding object as current object on the sensor
    private void OnTriggerExit(Collider other)
    {
        if (GameObject.ReferenceEquals(other.gameObject, currentObject))
        {
            measured = false;
            currentObject = null;
        }
    }

    // Get the mass of the object on the pressure sensor
    private float getMass()
    {
        // Should not be called without object, but returns 0 if done so
        if (currentObject == null)
        {
            return 0f;
        }
        
        measured = true;
        return currentObject.GetComponent<Rigidbody>().mass;
    }
}
