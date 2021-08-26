from __future__ import annotations
import argparse
import asyncio

from byzvis import ByzantineMessages, Message


async def main():
    my_parser = argparse.ArgumentParser(prog="byzvis", allow_abbrev=False)
    my_parser.add_argument('--time_window_time', action='store', type=int, help="Time between messages in milliseconds")
    my_parser.add_argument('--radius_factor', action='store', type=int, help="Radius increase factor by general")
    my_parser.add_argument('--source', action='store', type=str, help="CSV source file")
    args = my_parser.parse_args()

    bm = ByzantineMessages(messages=Message.from_csv(), time_window_time_ms=args.time_window_time or 500)
    bm.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
