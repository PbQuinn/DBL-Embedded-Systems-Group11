using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PusherDynTip : MonoBehaviour
{
    private Rigidbody rb;

    public List<GameObject> onPusher;

    public float speed;
    public float deltaTime;
    public Vector3 direction;

    private bool isSpaceDown = false;
    private bool isExtended = false;
    private bool isMoving = false;

    private float time = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown("space"))
        {
            isSpaceDown = true;
        }
    }

    // FixedUpdate is called once per physics update
    private void FixedUpdate()
    {
        foreach (GameObject o in onPusher)
        {
            o.GetComponent<Rigidbody>().velocity = speed * direction * Time.deltaTime;
        }

        if (isSpaceDown && ! isMoving)
        {
            if (! isExtended)
            {
                rb.velocity = speed * direction * Time.deltaTime;
                isMoving = true;
                isExtended = true;
                isSpaceDown = false;
            }
            else
            {
                rb.velocity = speed * -direction * Time.deltaTime;
                isMoving = true;
                isExtended = false;
                isSpaceDown = false;
            }
        }

        if (isMoving)
        {
            time += Time.fixedDeltaTime;

            if (time > deltaTime)
            {
                rb.velocity = Vector3.zero;
                isMoving = false;
                time = 0.0f;
            }
        }
    }

    // Add colliding object to onPusher
    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.tag != rb.tag) {
            onPusher.Add(collision.gameObject);
        }
    }

    // Remove colliding object from onPusher
    private void OnCollisionExit(Collision collision)
    {
        onPusher.Remove(collision.gameObject);
    }
}
