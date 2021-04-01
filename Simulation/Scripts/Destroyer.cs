using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Destroyer : MonoBehaviour
{
    // When something enters the destroyer
    private void OnTriggerEnter(Collider collider)
    {
        // Destroy it
        Destroy(collider.gameObject);
    }
}
