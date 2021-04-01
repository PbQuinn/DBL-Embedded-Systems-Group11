using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PusherKinTip : MonoBehaviour
{
    // Objects on the pusher
    public List<GameObject> onPusher;

    // Speed of pusher
    public float speed = 1.0f;

    // End and start position
    public Vector3 direction;

    // FixedUpdate is called once per physics update
    private void FixedUpdate()
    {
        foreach (GameObject o in onPusher)
        {
            o.GetComponent<Rigidbody>().velocity = speed * direction * Time.deltaTime;
        }
    }

    // Add colliding object to onPusher
    private void OnCollisionEnter(Collision collision)
    {
        onPusher.Add(collision.gameObject);
    }

    // Remove colliding object from onPusher
    private void OnCollisionExit(Collision collision)
    {
        onPusher.Remove(collision.gameObject);
    }
}
