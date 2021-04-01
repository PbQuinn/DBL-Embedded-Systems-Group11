using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SensorColor : MonoBehaviour
{
    // The communicator
    public GameObject communicator;

    // Current object under sensor
    public GameObject currentObject;

    // Time of scan duration
    public float deltaTime;

    // Time when scanning starts
    private float startTime;

    // Is the color sensor scanning?
    private bool isScanning = false;

    // Update is called once per frame
    void Update()
    {
        if (isScanning && (Time.time - startTime >= deltaTime))
        {
            isScanning = false;
            string color = GetColor();
            string output;
            if (name == "Primary Color")
            {
                output = "Primary " + color;
            }
            else
            {
                output = "Secondary " + color;
            }

            communicator.GetComponent<Communicator>().Communicate(output);
        }
    }

    // When something enters the range of the color sensor
    private void OnTriggerEnter(Collider collider)
    {
        currentObject = collider.gameObject;
    }

    // When something enters the range of the color sensor
    private void OnTriggerExit(Collider collider)
    {
        if (GameObject.ReferenceEquals(currentObject, collider.gameObject))
        {
            currentObject = null;
        }
    }

    // Set scanning to true or false
    public void Scan()
    {
        isScanning = true;
        startTime = Time.time;
    }

    // Get color of current object
    public string GetColor()
    {
        if (currentObject == null)
        {
            return "Neither";
        }
        else
        {
            return currentObject.GetComponent<Renderer>().material.name.Replace(" (Instance)", "");
        }
    }
}
