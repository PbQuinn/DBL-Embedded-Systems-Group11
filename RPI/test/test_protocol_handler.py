from unittest import TestCase
from requests import HTTPError
from RPI.src.protocol_handler import ProtocolHandler


class TestInit(TestCase):

    def test_login_exception(self):
        self.assertRaises(HTTPError, ProtocolHandler().login, "group11", "x")
        self.assertRaises(HTTPError, ProtocolHandler().login, "x", "0G1EH2HF28")
        self.assertRaises(HTTPError, ProtocolHandler().login, "x", "x")

    def test_can_pickup(self):
        self.protocol = ProtocolHandler()
        self.assertIsInstance(self.protocol.can_pickup(), bool)

    def test_inform_pickup(self):
        self.protocol = ProtocolHandler()
        self.assertIsInstance(self.protocol.inform_pickup(), bool)

    def test_inform_color(self):
        self.protocol = ProtocolHandler()
        self.protocol.inform_color(1)  # Black
        self.protocol.inform_color(0)  # White

    def test_inform_alive(self):
        self.protocol = ProtocolHandler()
        self.protocol.inform_alive()
