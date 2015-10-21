class Owner(object):
    def __init__(self, picks=[]):
        self.picks = picks

    def __str__(self):
        return "Owner with picks: " + str(self.picks)
