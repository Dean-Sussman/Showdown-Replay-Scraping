import os
import json
import re
import pprint
from collections import Counter

replays = []
chat_totals = Counter()

for file in os.listdir():
    if file.endswith(".json"):
        replays.append(file)

for replay in replays:
    with open(replay, "r") as f:
        data = json.load(f)
    chat_list = re.findall(r'\|c\|[^|]*', data["log"]) # finds all instances of '|c| [username]' in a game's log
    chat_list = list(map(lambda x: x[4:], chat_list)) # slices off the |c| and leading space/star character
    chat_counts = Counter(chat_list) # counts how many messages each chatter sent
    chat_totals.update(chat_counts) # adds most recent count to running total
pprint.pprint(chat_totals)