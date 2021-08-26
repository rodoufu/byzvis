from __future__ import annotations
import turtle
import math
import threading
from typing import Optional, List, Dict

from .message import Message
from .general_obj import General


class ByzantineMessages(object):
    def __init__(
            self, messages: List[Message], r: Optional[int] = None, factor: int = 10, time_window_time_ms: int = 500,
    ):
        self.time_window_time_ms = time_window_time_ms
        self.__wn = turtle.Screen()

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

        count = 0
        screen_size = self.__wn.screensize()
        for status, color in General.message_color.items():
            General(
                label=f"{status.to_str()}  ",
                pos=(-3 * screen_size[0] // 4, screen_size[1] - count * 30),
                color=color,
            )
            count += 1

        num_generals = max_generals + 1
        if not self.r:
            self.r = num_generals * factor
        self.generals = [
            General(label=f"G{x}", pos=(int(self.r * math.cos(x * 2 * math.pi / num_generals)),
                                        int(self.r * math.sin(x * 2 * math.pi / num_generals))))
            for x in range(num_generals)
        ]

        def reset():
            self.reset()
            self.__run_ontimer()

        self.__wn.onkey(reset, key='space')

    def __draw_messages(self) -> bool:
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

    def __run_ontimer(self):
        self.__wn.update()
        if self.__draw_messages():
            self.__wn.ontimer(lambda: self.__run_ontimer(), self.time_window_time_ms)

    def start(self):
        self.reset()
        self.__run_ontimer()
        turtle.listen()
        self.__wn.mainloop()
