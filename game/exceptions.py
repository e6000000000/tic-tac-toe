class IdException(Exception):
    def __init__(self, text=''):
        self.txt = text

class MoveUnableException(Exception):
    def __init__(self, text=''):
        self.txt = text