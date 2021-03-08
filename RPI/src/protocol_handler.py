import requests


class ProtocolHandler:
    """Class used as interface for communicating with the protocol

        Attributes
        __________
        token : string
            the token used for authorization when communicating with the
            protocol, obtained upon initialization

        Methods
        _______
        can_pickup() : bool
            returns true iff next disk may be retrieved
        inform_pickup() : bool
            informs the protocol that a disk has been retrieved,
            returns whether this was according to protocol
        inform_color(int) : void
            informs the protocol of the color of the retrieved disk
        inform_alive() : void
            informs the protocol of the fact that this system is still alive
        """

    def __init__(self, username="group11", password="0G1EH2HF28"):
        """Connects to the protocol and gets token upon initialization

        @param username  the username to login with, 'group11' by default
        @param password  the password to login with, '0G1EH2HF28' by default
        @modifies self.token
        """

        credentials = {"User": username, "Password": password}
        login_attempt = requests.post(
            "https://brokenprotocol.xyz/Authentication/Login",
            json=credentials,
            headers={"Content-Type": "application/json"}
        )
        login_attempt.raise_for_status()
        self.token = login_attempt.json()["Token"]

    def can_pickup(self):
        """Returns true iff next disk may be retrieved
        """

        permission = requests.get(
            "https://brokenprotocol.xyz/Device/CanPickup",
            headers={"auth": self.token}
        )
        permission.raise_for_status()
        return permission.json()

    def inform_pickup(self):
        """Informs the protocol that a disk has been retrieved

        @returns true if this was according to protocol, otherwise false
        """

        permission = requests.post(
            "https://brokenprotocol.xyz/Device/PickedUpObject",
            headers={"auth": self.token}
        )
        permission.raise_for_status()
        return permission.json()

    def inform_color(self, color):
        """Informs the protocol of the color of the retrieved disk

        @param color  the color of the retrieved disk
        """

        response = requests.post(
            "https://brokenprotocol.xyz/Device/DeterminedObject",
            json={"Color": color},
            headers={
                "auth": self.token,
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()

    def inform_alive(self):
        """Informs the protocol of the fact that this system is still alive
        """

        response = requests.get(
            "https://brokenprotocol.xyz/Device/Heartbeat",
            headers={"auth": self.token}
        )
        response.raise_for_status()

