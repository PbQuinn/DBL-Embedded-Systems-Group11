using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Stringer : MonoBehaviour
{
    // Location to teleport object to
    public Vector3 location;

    // Offset (width of disk)
    public float offset;

    // Number of stringed disks
    private int number_stringed = 0;

    // When the stringer touches something
    private void OnTriggerEnter(Collider collider)
    {
        // Take colliding object
        GameObject obj = collider.gameObject;

        // Rotate it
        obj.transform.eulerAngles = new Vector3(
            0,
            0,
            0
        );

        Vector3 destination = location + (Vector3.up * offset * number_stringed);

        // Teleport it
        obj.transform.position = destination;

        // Update number of stringed disks
        number_stringed++;
    }
}
