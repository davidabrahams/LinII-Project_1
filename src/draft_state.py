from pick import Pick
from player import Player
from owner import Owner

class DraftState(object):

    round_length = 10
    num_rounds = 16

    def __init__(self, qbs, rbs, wrs, tes, dsts, ks, round_number=1,
                 pick_number=1, taken=[], owners=[]):
        # taken is a list of rounds, where each round is a list of the players
        # taken in that rounds
        self.round_number = round_number
        self.pick_number = pick_number
        self.taken = taken

        self.owners = owners
         # if no owners inputed, initalize the array of owners
        if self.owners is []:
            self.owners = self.init_owners()

        # place available players in a dictionary
        self.available = {'qbs': qbs, 'rbs': rbs, 'wrs': wrs, 'tes': tes,
                          'dsts': dsts, 'ks': ks}

    def __str__(self):
        return "Round #" + str(self.round_number) + ", Pick #" +\
               str(self.pick_number) + ", Players taken: " + str([t.identifier
                                                                  for t in
                                                                  self.taken])

    def init_owners(self):
        """
        >>> state = DraftState([], [], [], [], [], [])
        >>> owners = state.init_owners()
        >>> for o in owners:
        ...     print o
        """
        owners = []
        # i is the owner number
        for i in range(1, self.round_length + 1):
            picks = []
            # j is the round number
            for j in range(self.num_rounds):
                if j % 2 == 0:
                    pick = i + self.round_length * j
                else:
                    pick = self.round_length - i + 1 + self.round_length * j
                picks.append(pick)

            owner = Owner(picks)
            owners.append(owner)
        return owners

    def get_available_picks(self):
        """
        >>> state = DraftState([Player('qb', 100, 'qb1'), Player('qb', 90, 'qb2')], [Player('rb', 100, 'rb1')], [], [], [], [])
        >>> picks = state.get_available_picks()
        >>> for p in picks:
        ...     print p.identifier
        qb1
        rb1

        """
        avail_picks = []
        for players in self.available.itervalues():
            if len(players) > 0:
                avail_picks.append(players[0].identifier)

        return [Pick(identifier) for identifier in avail_picks]

    def next_state(self, pick):
        """
        >>> state = DraftState([Player('qb', 100, 'qb1'), Player('qb', 90, 'qb2')], [Player('rb', 100, 'rb1')], [], [], [], [])
        >>> pick = Pick('qb1')
        >>> next_state = state.next_state(pick)
        >>> print next_state
        Round #1, Pick #2, Players taken: ['qb1']

        """

        # create copies
        avail_dict = dict(self.available)
        taken = list(self.taken)

        for player_list in avail_dict.itervalues():

            player_ids = [p.identifier for p in player_list]

            if pick.identifier in player_ids:
                index_to_remove = player_ids.index(pick.identifier)
                removed = player_list.pop(index_to_remove)
                taken.append(removed)

        next_pick = self.pick_number + 1
        next_round = (self.pick_number - 1) / 10 + 1

        return DraftState(avail_dict['qbs'], avail_dict['rbs'],
                          avail_dict['wrs'], avail_dict['tes'],
                          avail_dict['dsts'], avail_dict['ks'],
                          next_round, next_pick, taken)


    def is_draft_over(self):
        return len(self.taken) >= self.round_number * DraftState.round_length


    # def max(self, game_state):
    #     picks = game_state.get_available_picks()

    #     best_pick = picks[0]
    #     best_score = float('-inf')


    def eval_state():
        pass

    def get_team(self, owner):
        """This function returns the players on an owner's team at the current
        draf state.
        """
        players = []
        for pick in owner.picks:
            if pick <= len(self.taken):
                players.append(self.taken[pick - 1])



#TODO
# Evaluate Team function (Heuristic)
# Max function --> based on evaluate function
