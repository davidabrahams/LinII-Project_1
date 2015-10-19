from move import Move
from player import Player

class DraftState(object):

    def __init__(self, qbs, rbs, wrs, tes, dsts, ks):
        # taken is a list of rounds, where each round is a list of the players
        # taken in that rounds
        self.taken = [[]]
        # place available players in a dictionary
        self.available = {'qbs': qbs, 'rbs': rbs, 'wrs': wrs, 'tes': tes,
                          'dsts': dsts, 'k': ks}

    def get_available_picks(self):
        """
        >>> state = DraftState([Player('qb', 100, 'qb1'), Player('qb', 90, 'qb2')], [Player('rb', 100, 'rb1')], [], [], [], [])
        >>> moves = state.get_available_picks()
        >>> for m in moves:
        ...     print m.identifier
        qb1
        rb1

        """
        avail_picks = []
        for players in self.available.itervalues():
            if len(players) > 0:
                avail_picks.append(players[0].identifier)

        return [Move(identifier) for identifier in avail_picks]
