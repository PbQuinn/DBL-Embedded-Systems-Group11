using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Conveyor : MonoBehaviour
{
    // Speed of the conveyor belt
    public float speed;

    // Direction of the conveyor belt
    public Vector3 direction;

    // Whether the conveyor belt is enabled
    private bool isEnabled = true;

    // Objects that are on the conveyor belt
    public List<GameObject> onBelt;

    // Manually deleted objects
    public List<GameObject> deleted;

    // FixedUpdate is called once per physics update
    private void FixedUpdate()
    {
        if (isEnabled)
        {
            foreach (GameObject o in onBelt)
            {
                if (o == null)
                {
                    deleted.Add(o);
                } else {
                    o.GetComponent<Rigidbody>().velocity = speed * direction * Time.deltaTime;
                }
            }

            // Remove deleted objects
            foreach (GameObject o in deleted) {
                onBelt.Remove(o);
            }
            deleted.Clear();
        }
    }

    // Add colliding object to onBelt
    private void OnCollisionEnter(Collision collision)
    {
        onBelt.Add(collision.gameObject);
    }

    // Remove colliding object from onBelt
    private void OnCollisionExit(Collision collision)
    {
        onBelt.Remove(collision.gameObject);
    }

    // Enable or disable the conveyor belt
    public void SetEnabled(bool isEnabled)
    {
        this.isEnabled = isEnabled;
    }

    // Returns whether conveyor belt is enabled
    public bool GetEnabled()
    {
        return isEnabled;
    }
}
