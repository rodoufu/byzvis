from __future__ import annotations
import turtle
import math
import json
import threading
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

    def to_str(self) -> str:
        if self == MessageStatus.Success:
            return "Success"
        elif self == MessageStatus.NotDelivered:
            return "Not delivered"
        elif self == MessageStatus.Tampered:
            return "Tampered"
        else:
            raise Exception("Unexpected message status")


class General(object):
    message_color = {
        MessageStatus.Success: "blue",
        MessageStatus.NotDelivered: "red",
        MessageStatus.Tampered: "yellow",
    }

    def __init__(self, label: str, pos: Tuple[int, int] = (0, 0), color: Optional[str] = None):
        self.normal_color = color or 'black'
        self.clicked_color = 'yellow'

        self.obj = turtle.Turtle()
        self.obj.color(self.normal_color)
        self.obj.shape('circle')
        self.obj.penup()
        current_pos = self.obj.pos()
        self.obj.goto(pos[0] + current_pos[0], pos[1] + current_pos[1])
        self.obj.write(label, True, align="right", font=("arial", 15, "bold"))

        def on_click(x, y):
            self.obj.color(self.clicked_color)

        self.obj.onclick(on_click)

        def on_release(x, y):
            self.obj.clear()
            self.obj.color(self.normal_color)
            self.obj.goto((x, y))
            self.obj.write(label, True, align="right", font=("arial", 15, "bold"))

        self.obj.onrelease(on_release)

    def send_msg(self, general: General, status: MessageStatus, pen: turtle.Pen):
        if status == MessageStatus.Unexpected:
            raise Exception("Unexpected message status")
        if general == self:
            raise Exception("A general cannot send a message to itself")

        pen.penup()
        pen.goto(*self.obj.pos())
        pen.showturtle()
        pen.color(General.message_color[status])
        pen.penup()
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
        self.__draw_lock = threading.Lock()

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
            General(label=f"G{x}", pos=(int(self.r * math.cos(x * 2 * math.pi / num_generals)),
                                        int(self.r * math.sin(x * 2 * math.pi / num_generals))))
            for x in range(num_generals)
        ]

        count = 0
        for status, color in General.message_color.items():
            General(
                label=f"{status.to_str()}  ",
                pos=(num_generals * factor - 250, num_generals * factor - count * 30 + 350),
                color=color,
            )
            count += 1

    def draw_messages(self) -> bool:
        with self.__draw_lock:
            if self.current_time > self.max_time:
                self.pen.clear()
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

    def reset(self):
        with self.__draw_lock:
            self.current_time = 0
