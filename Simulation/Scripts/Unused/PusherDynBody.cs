using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PusherDynBody : MonoBehaviour
{
    private Rigidbody rb;

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
}
