import os
import json
import re
from collections import Counter
import pprint

def clean_move_list(move_list, name_one, name_two):
    alt_list = []
    for move in move_list:
        move = move[5:] # slice off 'move|'
        move = move.replace("p1a", name_one) # replace 'p1a|' with the player's name
        move = move.replace("p2a", name_two) # same as above but for p2a
        move = move.replace(":", "|") # player: mon|move --> player| mon|move
        player_move = move.split("|")[0] + ":" + move.split("|")[2]
        alt_list.append(player_move)
    return alt_list


replays = []
chat_totals = Counter() # tracks how many times each player sent a chat message
player_move_totals = Counter() # tracks player+move combos (e.g. {player} used stealth rocks 20 times)
only_move_totals = Counter() # tracks just move counts (e.g. stealth rocks was used 120 times)

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

    p1 = data["players"][0]
    p2 = data["players"][1]
    move_list = re.findall(r'move\|[^|]*\|[^|]*', data["log"]) # finds all instances of 'move|pX: mon|movename'
    player_move_list = clean_move_list(move_list, p1, p2) # clean up list entries to look like 'playername:movename'
    player_move_count = Counter(player_move_list)
    player_move_totals.update(player_move_count)
    only_move_list = list(map(lambda x: x.split(":")[1], player_move_list)) # raw count of moves, no player association
    only_move_totals.update(only_move_list)

# pprint.pprint(player_move_totals)
# pprint.pprint(only_move_totals)

# below prints separate with tab character to make porting to excel easier, uncomment as needed

# for chatter, count in chat_totals.items():
#     print(chatter, "\t", count)

# for movecombo, count in player_move_totals.items():
#     print(movecombo, "\t", count)

# for movecombo, count in only_move_totals.items():
#     print(movecombo, "\t", count)