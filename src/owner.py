from pick import Pick
from player import Player
import draft_state
import random
import numpy as np

class Owner(object):

    def __init__(self, picks=[], strategy='most_points', name=None):
        self.picks = picks
        self.strategy = strategy
        self.position_maxes = {'qb': 2, 'rb': 5, 'wr': 5,
                               'te': 2, 'dst': 1, 'k': 1}
        self.starters = {'qb': 1, 'rb': 2, 'wr': 3,
                         'te': 2, 'dst': 1, 'k': 1}
        self.name = self.strategy + " " + name
        if self.name is None:
            self.name = self.strategy

    def set_strat(self, strat, owner_num):
        self.name = strat + " " + str(owner_num)
        self.strategy = strat

    def __str__(self):
        return "Owner with picks: " + str(self.picks)

    def multiplier(self, position, my_team):
        return 1.0 - 0.2 * max(len(my_team[position]) + 1 -
                               self.starters[position], 0)

    def multiplier_nums(self, starters, num):
        return 1.0 - 0.2 * max(num - starters, 0)


    def make_decision(self, draft_state, replacement_lvls=None):
        """
        Returns a Pick object
        >>> state = draft_state.DraftState({'qb': [Player('qb', 110, 'qb1'), Player('qb', 102, 'qb2')], 'rb': [Player('rb', 121, 'rb1'), Player('rb', 50, 'rb2')], 'wr': [Player('wr', 80, 'wr1')], 'te': [Player('te', 90, 'te1')], 'dst': [Player('dst', 40, 'dst1')], 'k': [Player('k', 20, 'k1')]})
        >>> owner = state.owners[0]
        >>> owner.make_decision(state).identifier
        'rb1'
        >>> owner.strategy = "worst_dropoff"
        >>> owner.make_decision(state).identifier
        'te1'
        >>> state.available['qb'][0].value = 230
        >>> owner.make_decision(state).identifier
        'qb1'

        """

        player_to_pick = None
        my_team = draft_state.get_team(self)
        available = draft_state.available

        # Control function --> picks a random position and the best player at that position
        if self.strategy == 'control':
            choices = []
            for position, players in available.iteritems():
                if (len(players) > 0 and len(my_team[position])
                    < self.position_maxes[position]):
                    player = players[0]
                    choices.append(player)

            player_to_pick = random.choice(choices)

        if self.strategy == 'control_weighted':
            choices = []
            random_weights = []
            for position, players in available.iteritems():
                if (len(players) > 0 and len(my_team[position])
                    < self.position_maxes[position]):
                    player = players[0]
                    choices.append(player)
                    random_weights.append(self.position_maxes[position])
            random_weights = np.array(random_weights)
            random_weights = [float(r) / sum(random_weights)
                              for r in random_weights]
            player_to_pick = np.random.choice(choices, p=random_weights)

        if self.strategy == 'most_points':
            max_points = 0
            for position, players in available.iteritems():
                if (len(players) > 0 and len(my_team[position])
                    < self.position_maxes[position]):
                    player = players[0]
                    player_val = player.value
                    if player_val > max_points:
                        max_points = player_val
                        player_to_pick = player

        # Worst dropoff to second best available
        if self.strategy == 'worst_dropoff':
            difference = 0
            for position, players in available.iteritems():
                if (len(players) > 0 and len(my_team[position])
                    < self.position_maxes[position]):
                    player = players[0]
                    player_val = player.value
                    if len(players) == 1:
                        if player_val > difference:
                            difference = player_val
                            player_to_pick = player
                    elif len(players) > 1:
                        player_compare = players[1]
                        player_val_compare = player_compare.value
                        difference_local = player_val - player_val_compare
                        if difference_local > difference:
                            difference = difference_local
                            player_to_pick = player

        # Worst dropoff to guaranteed player
        if self.strategy == 'worst_guaranteed':
            difference = 0
            current_pick_index = self.picks.index(draft_state.pick_number)
            for position, players in available.iteritems():
                if (len(players) > 0 and len(my_team[position])
                    < self.position_maxes[position]):
                    player = players[0]
                    player_val = player.value
                    worst_guaranteed_val = 0
                    # there is a next pick
                    if current_pick_index + 1 < len(self.picks):

                        # number of people who pick before me
                        picks_to_pass = (self.picks[current_pick_index + 1] -
                                         self.picks[current_pick_index] - 1)
                        # there will be a player available next time I pick
                        if picks_to_pass < len(players) and picks_to_pass != 0:
                            worst_guaranteed_player = players[picks_to_pass]
                            worst_guaranteed_val = worst_guaranteed_player.value
                    # if this difference is higher than the previous seen diff
                    # pick the player at this position
                    if player_val - worst_guaranteed_val > difference:
                        difference = player_val - worst_guaranteed_val
                        player_to_pick = player

        # value over replacement
        if self.strategy == 'vorp' or self.strategy == 'pos_vorp':
            highest_vorp = -float('inf')
            for position, players in available.iteritems():
                if (len(players) > 0 and len(my_team[position])
                    < self.position_maxes[position]):
                    # print "Examining position " + position
                    player = players[0]
                    player_val = player.value
                    vorp = player_val - replacement_lvls[player.position]
                    if self.strategy == 'pos_vorp':
                        mult = self.multiplier(position, my_team)
                        vorp = mult * vorp
                    if vorp > highest_vorp:
                        player_to_pick = player
                        highest_vorp = vorp


        return Pick(player_to_pick.identifier)

    def eval_team(self, draft_state):
        score = 0.0
        my_team = draft_state.get_team(self)
        for pos in my_team:
            for i, player in enumerate(my_team[pos]):
                mult = self.multiplier_nums(self.starters[pos], i + 1)
                score += player.value * mult

        return score


