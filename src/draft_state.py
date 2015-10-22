from pick import Pick
from player import Player
from owner import Owner

class DraftState(object):

    round_length = 10
    num_rounds = 16

    def __init__(self, available, round_number=1,
                 pick_number=1, taken=[], owners=[]):
        # taken is a list of rounds, where each round is a list of the players
        # taken in that rounds
        self.round_number = round_number
        self.pick_number = pick_number
        self.taken = taken

        self.owners = owners
         # if no owners inputed, initalize the array of owners
        if len(self.owners) == 0:
            self.owners = self.init_owners()

        # place available players in a dictionary
        self.available = available

    def __str__(self):
        return "Round #" + str(self.round_number) + ", Pick #" + \
               str(self.pick_number) + ", Players taken: " + str([t.identifier
                                                                  for t in
                                                                  self.taken])

    def init_owners(self):
        """
        >>> state = DraftState({})
        >>> owners = state.init_owners()
        >>> for o in owners:
        ...     print o
        Owner with picks: [1, 20, 21, 40, 41, 60, 61, 80, 81, 100, 101, 120, 121, 140, 141, 160]
        Owner with picks: [2, 19, 22, 39, 42, 59, 62, 79, 82, 99, 102, 119, 122, 139, 142, 159]
        Owner with picks: [3, 18, 23, 38, 43, 58, 63, 78, 83, 98, 103, 118, 123, 138, 143, 158]
        Owner with picks: [4, 17, 24, 37, 44, 57, 64, 77, 84, 97, 104, 117, 124, 137, 144, 157]
        Owner with picks: [5, 16, 25, 36, 45, 56, 65, 76, 85, 96, 105, 116, 125, 136, 145, 156]
        Owner with picks: [6, 15, 26, 35, 46, 55, 66, 75, 86, 95, 106, 115, 126, 135, 146, 155]
        Owner with picks: [7, 14, 27, 34, 47, 54, 67, 74, 87, 94, 107, 114, 127, 134, 147, 154]
        Owner with picks: [8, 13, 28, 33, 48, 53, 68, 73, 88, 93, 108, 113, 128, 133, 148, 153]
        Owner with picks: [9, 12, 29, 32, 49, 52, 69, 72, 89, 92, 109, 112, 129, 132, 149, 152]
        Owner with picks: [10, 11, 30, 31, 50, 51, 70, 71, 90, 91, 110, 111, 130, 131, 150, 151]
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
        >>> state = DraftState({'qbs': [Player('qb', 100, 'qb1'), Player('qb', 90, 'qb2')], 'rbs': [Player('rb', 100, 'rb1')], 'wrs': [], 'tes': [], 'dsts': [], 'ks': []})
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
        >>> state = DraftState({'qbs': [Player('qb', 100, 'qb1'), Player('qb', 90, 'qb2')], 'rbs': [Player('rb', 100, 'rb1')], 'wrs': [], 'tes': [], 'dsts': [], 'ks': []})
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

        return DraftState(avail_dict,
                          next_round, next_pick, taken)


    def is_draft_over(self):
        return len(self.taken) >= self.round_number * DraftState.round_length


    # def max(self, game_state):
    #     picks = game_state.get_available_picks()

    #     best_pick = picks[0]
    #     best_score = float('-inf')


    def eval_state():
        # TODO:
        # get the owner who just picked (I think)
        # evaluate his team
        # return it
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
