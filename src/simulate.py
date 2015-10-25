import os
import pandas as pd
import draft_state
from player import Player
from draft_state import DraftState

toplevel_dir = os.path.join(os.path.dirname(__file__), os.path.pardir)
CSV_FILENAME = os.path.join(toplevel_dir, "data", "projections.csv")
OUTPUT_FN = os.path.join(toplevel_dir, "data", "table.csv")

replacement_lvls = {'qb': 14, 'rb': 35, 'wr': 37,
                    'te': 7, 'dst': 5, 'k': 2}

def load_csv(fn):
    return pd.read_csv(fn)

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

    print_teams(current_state)

def print_teams(end_state):
    owners = end_state.owners
    positions = ['qb', 'rb', 'wr', 'te', 'dst', 'k']
    df = pd.DataFrame(index=['qb1', 'rb1', 'rb2', 'wr1', 'wr2', 'wr3', 'te1', 'dst', 'k', 'qb2', 'rb3', 'rb4', 'rb5','wr4', 'wr5', 'te2', 'score'])
    for o in owners:
        team = end_state.get_team(o)
        o_team = []
        o_team.append(team['qb'][0].value)
        o_team.append(team['rb'][0].value)
        o_team.append(team['rb'][1].value)
        o_team.append(team['wr'][0].value)
        o_team.append(team['wr'][1].value)
        o_team.append(team['wr'][2].value)
        o_team.append(team['te'][0].value)
        o_team.append(team['dst'][0].value)
        o_team.append(team['k'][0].value)
        o_team.append(team['qb'][1].value)
        o_team.append(team['rb'][2].value)
        o_team.append(team['rb'][3].value)
        o_team.append(team['rb'][4].value)
        o_team.append(team['wr'][3].value)
        o_team.append(team['wr'][4].value)
        o_team.append(team['te'][1].value)
        o_team.append(o.eval_team(end_state))
        df[o.name] = o_team

    print df
    df.to_csv(OUTPUT_FN)




if __name__ == '__main__':
    main()
