class Pick(object):

    # id is player who was drafted
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return self.identifier
