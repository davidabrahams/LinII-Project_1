import os
import pandas
import draft_state
from player import Player
from draft_state import DraftState

toplevel_dir = os.path.join(os.path.dirname(__file__), os.path.pardir)
CSV_FILENAME = os.path.join(toplevel_dir, "data", "projections.csv")

replacement_lvls = {'qb': 14, 'rb': 35, 'wr': 37,
                    'te': 7, 'dst': 5, 'k': 2}

def load_csv(fn):
    return pandas.read_csv(fn)

def get_replacement_lvls(player_dict, replacements):
    res = {}
    for k in replacements:
        res[k] = player_dict[k][replacements[k]].value
    return res

def main():
    df = load_csv(CSV_FILENAME)
    starting_players = draft_state.empty_state()

    for _, row in df.iterrows():
        pos = row['Position'].lower()
        val = row['Fantasy Points']
        identifier = pos + str(row['Identifier'])
        key = pos
        player = Player(pos, val, identifier)
        starting_players[key].append(player)

    replacement_vals = get_replacement_lvls(starting_players, replacement_lvls)

    start_draft_state = DraftState(starting_players)
    current_state = start_draft_state

    while not current_state.is_draft_over():
        current_owner = current_state.whos_pick()
        pick = current_owner.make_decision(current_state, replacement_vals)
        print "At pick number: " + str(current_state.pick_number) + " " + str(pick) + " was selected."
        current_state = current_state.next_state(pick)

if __name__ == '__main__':
    main()
