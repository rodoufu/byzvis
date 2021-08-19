from __future__ import annotations
import asyncio
import turtle

from bft import ByzantineMessages, Message, MessageStatus


def run_ontimer(wn: turtle.Screen, bm: ByzantineMessages, next_time: int):
    wn.update()
    if bm.draw_messages():
        wn.ontimer(lambda: run_ontimer(wn, bm, next_time), next_time)


async def main():
    wn = turtle.Screen()
    time_window_time_ms = 500

    messages = [Message(1, 0, MessageStatus.Tampered, 1), Message(0, 1, MessageStatus.Success, 0)]

    bm = ByzantineMessages(messages)
    run_ontimer(wn, bm, time_window_time_ms)

    wn.mainloop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
