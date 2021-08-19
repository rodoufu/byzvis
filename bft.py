from __future__ import annotations
import turtle
import math
import json
from typing import Tuple, Optional, List, Dict
from enum import IntEnum


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


class General(object):
    message_color = {
        MessageStatus.Success: "blue",
        MessageStatus.NotDelivered: "red",
        MessageStatus.Tampered: "yellow",
    }

    def __init__(self, pos: Tuple[int, int] = (0, 0)):
        self.obj = turtle.Turtle()
        self.obj.shape('circle')
        self.obj.penup()
        current_pos = self.obj.pos()
        self.obj.goto(pos[0] + current_pos[0], pos[1] + current_pos[1])

    def send_msg(self, general: General, status: MessageStatus, pen: turtle.Pen):
        if status == MessageStatus.Unexpected:
            raise Exception("Unexpected message status")
        if general == self:
            raise Exception("A general cannot send a message to itself")

        pen.showturtle()
        pen.color(General.message_color[status])
        pen.penup()
        pen.goto(*self.obj.pos())
        pen.pendown()
        pen.goto(*general.obj.pos())
        pen.hideturtle()

    def __str__(self) -> str:
        pos = self.obj.pos()
        return json.dumps({
            "x": pos[0],
            "1": pos[1],
        })


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


class ByzantineMessages(object):
    def __init__(self, messages: List[Message], r: Optional[int] = None, factor: int = 10):
        self.time_messages: Dict[int, List[Message]] = {}
        self.max_time = 0
        self.pen = turtle.Pen()
        self.pen.hideturtle()
        self.current_time = 0
        self.r = r

        max_generals = 0

        for message in messages:
            max_generals = max([max_generals, message.source, message.target])

            self.max_time = max(self.max_time, message.moment)
            list_msg = self.time_messages.get(message.moment, [])
            list_msg.append(message)

            self.time_messages[message.moment] = list_msg

        num_generals = max_generals + 1
        if not self.r:
            self.r = num_generals * factor
        self.generals = [
            General(pos=(int(self.r * math.cos(x * 2 * math.pi / num_generals)),
                         int(self.r * math.sin(x * 2 * math.pi / num_generals))))
            for x in range(num_generals)
        ]

    def draw_messages(self) -> bool:
        if self.current_time > self.max_time:
            print("Done processing images")
            return False
        current_messages = self.time_messages[self.current_time]
        self.pen.clear()

        for message in current_messages:
            source = self.generals[message.source]
            target = self.generals[message.target]
            source.send_msg(target, message.status, self.pen)

        self.current_time += 1
        return True
