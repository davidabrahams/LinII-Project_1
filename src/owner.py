class Owner(object):

    def __init__(self, picks=[], strategy='most_points'):
        self.picks = picks
        self.strategy = strategy

    def __str__(self):
        return "Owner with picks: " + str(self.picks)

    def make_decision(self, draft_state):
        """This function takes in the current draft state and returns the
        player the owner would pick. For example, if all QBs are available and
        the owner drafts a qb, the function would return the str 'qb1'.
        """
        my_team = draft_state.get_team(self)
        if strategy == 'most_points':
            pass
        # Worst dropoff to second best available
        if strategy == 'worst_dropoff':
            pass
        # Worst dropoff to guaranteed player
        if strategy == 'worst_guaranteed'
        pass
