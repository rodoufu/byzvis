from __future__ import annotations
import argparse
import asyncio
import csv
from typing import List

from bft import ByzantineMessages, Message, MessageStatus


async def main():
    my_parser = argparse.ArgumentParser(prog="byzvis", allow_abbrev=False)
    my_parser.add_argument('--time_window_time', action='store', type=int, help="Time between messages in milliseconds")
    my_parser.add_argument('--radius_factor', action='store', type=int, help="Radius increase factor by general")
    my_parser.add_argument('--source', action='store', type=str, help="CSV source file")
    args = my_parser.parse_args()

    time_window_time_ms = args.time_window_time or 500
    source_file = args.source
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

    bm = ByzantineMessages(messages)
    bm.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
