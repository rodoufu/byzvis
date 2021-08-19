from unittest import TestCase

from .message import MessageStatus


class TestMessageStatus(TestCase):
    def test_from_int(self):
        self.assertEqual(MessageStatus.Unexpected, MessageStatus.from_int(0))
        self.assertEqual(MessageStatus.Success, MessageStatus.from_int(1))
        self.assertEqual(MessageStatus.NotDelivered, MessageStatus.from_int(2))
        self.assertEqual(MessageStatus.Tampered, MessageStatus.from_int(3))
