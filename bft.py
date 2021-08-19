from __future__ import annotations
import turtle
import json
from typing import Tuple, Optional, List, Dict
from enum import Enum


class MessageStatus(Enum):
    Unexpected = 0
    Success = 1
    NotDelivered = 2
    Tampered = 3


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
        self.pen = turtle.Pen()

    def send_msg(self, general: General, status: MessageStatus, pen: Optional[turtle.Pen] = None):
        if status == MessageStatus.Unexpected:
            raise Exception("Unexpected message status")
        if general == self:
            raise Exception("A general cannot send a message to itself")

        if not pen:
            pen = self.pen
        pen.hideturtle()
        pen.color(General.message_color[status])
        pen.penup()
        pen.goto(*self.obj.pos())
        pen.pendown()
        pen.goto(*general.obj.pos())

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
    def __init__(self, messages: List[Message]):
        self.time_messages: Dict[int, List[Message]] = {}
        self.max_time = 0
        self.pen = turtle.Pen()
        self.current_time = 0

        max_generals = 0

        for message in messages:
            max_generals = max([max_generals, message.source, message.target])

            self.max_time = max(self.max_time, message.moment)
            list_msg = self.time_messages.get(message.moment, [])
            list_msg.append(message)

            self.time_messages[message.moment] = list_msg

        self.generals = [General((x * 50, 0)) for x in range(max_generals + 1)]

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
