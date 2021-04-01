using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cameras : MonoBehaviour
{
    public Camera camConveyor;
    public Camera camStringer;

    void Start()
    {
        camConveyor.enabled = true;
        camStringer.enabled = false;
    }

    void Update()
    {

        if (Input.GetKeyDown(KeyCode.C))
        {
            camConveyor.enabled = !camConveyor.enabled;
            camStringer.enabled = !camStringer.enabled;
        }
    }
}
