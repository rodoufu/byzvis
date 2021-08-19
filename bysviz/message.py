from __future__ import annotations
import csv
import json
from enum import IntEnum
from typing import List, Optional


class MessageStatus(IntEnum):
    Unexpected = 0
    Success = 1
    NotDelivered = 2
    Tampered = 3

    @staticmethod
    def from_int(value: int) -> MessageStatus:
        possible_values = {int(x): x for x in MessageStatus}
        resp = possible_values.get(value)
        if resp is None:
            raise Exception(f"Invalid value {value} for MessageStatus")
        return resp

    def to_str(self) -> str:
        if self == MessageStatus.Success:
            return "Success"
        elif self == MessageStatus.NotDelivered:
            return "Not delivered"
        elif self == MessageStatus.Tampered:
            return "Tampered"
        else:
            raise Exception("Unexpected message status")


class Message(object):
    def __init__(self, source: int, target: int, status: MessageStatus, moment: int):
        self.source = source
        self.target = target
        self.status = status
        self.moment = moment

        if self.source < 0 or self.target < 0:
            raise Exception(f"Invalid message source or target: {self}")

    def __str__(self) -> str:
        return json.dumps(self)

    @staticmethod
    def from_csv(source_file: Optional[str] = None) -> List[Message]:
        messages: List[Message] = []
        if source_file:
            with open(source_file, newline='') as csv_file:
                spam_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                for row in spam_reader:
                    messages.append(Message(
                        int(row['source']), int(row['target']), MessageStatus.from_int(int(row['status'])),
                        int(row['moment']),
                    ))
        else:
            messages = [Message(1, 0, MessageStatus.Tampered, 1), Message(0, 1, MessageStatus.Success, 0)]
        return messages
