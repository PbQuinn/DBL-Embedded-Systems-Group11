using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawner : MonoBehaviour
{
    // Black object
    public Transform black;

    // White object
    public Transform white;

    // Key for spawning white
    public string keyWhite;

    // Key for spawning black
    public string keyBlack;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(keyWhite))
        {
            Spawn(black);
        }

        if (Input.GetKeyDown(keyBlack))
        {
            Spawn(white);
        }
    }

    // Spawn given prefab
    public void Spawn(Transform prefab)
    {
        Instantiate(prefab, transform.position, transform.rotation);
    }
}
