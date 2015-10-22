from pick import Pick
from player import Player
import draft_state

class Owner(object):

    def __init__(self, picks=[], strategy='most_points'):
        self.picks = picks
        self.strategy = strategy

    def __str__(self):
        return "Owner with picks: " + str(self.picks)

    def make_decision(self, draft_state):
        """

        >>> state = draft_state.DraftState({'qbs': [Player('qb', 110, 'qb1'), Player('qb', 90, 'qb2')], 'rbs': [Player('rb', 121, 'rb1')], 'wrs': [], 'tes': [], 'dsts': [], 'ks': []})
        >>> owner = state.owners[0]
        >>> owner.make_decision(state).identifier
        'rb1'
        >>> state.available['qbs'][0].value = 230
        >>> owner.make_decision(state).identifier
        'qb1'
        """

        player_to_pick = None
        my_team = draft_state.get_team(self) # currently unused
        available = draft_state.available
        if self.strategy == 'most_points':
            max_points = 0
            for position, players in available.iteritems():
                if len(players) > 0:
                    player = players[0]
                    player_val = player.value
                    if player_val > max_points:
                        max_points = player_val
                        player_to_pick = player
        # Worst dropoff to second best available
        if self.strategy == 'worst_dropoff':
            pass
        # Worst dropoff to guaranteed player
        if self.strategy == 'worst_guaranteed':
            pass

        return Pick(player_to_pick.identifier)
