from __future__ import annotations
import turtle
import json
from typing import Tuple, Optional

from .message import MessageStatus


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
