using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Funnel : MonoBehaviour
{
    // Location to teleport object to
    public Vector3 locationFunnel;

    // Location to teleport object to
    public Vector3 locationStringer;

    public GameObject stringer;

    // Disks in funnel
    public List<GameObject> inFunnel;

    // When something enters the teleporter
    private void OnTriggerEnter(Collider collider)
    {
        // Take disk
        GameObject obj = collider.gameObject;

        // Make it kinematic
        obj.GetComponent<Rigidbody>().isKinematic = true;

        // Rotate it
        obj.transform.eulerAngles = new Vector3(
            90,
            0,
            0
        );

        // Teleport it to funnel
        obj.transform.position = locationFunnel;

        // Add it to funnel
        inFunnel.Add(obj);
    }

    public void Next()
    {
        while (inFunnel.Count > 0 && inFunnel[0] == null)
        {
            inFunnel.Remove(inFunnel[0]);
        }

        if (inFunnel.Count > 0)
        {
            // Take first disk
            GameObject obj = inFunnel[0];

            // Teleport it to stringer
            obj.transform.position = locationStringer;

            // Remove it from funnel
            inFunnel.Remove(obj);
        }
    }
}
