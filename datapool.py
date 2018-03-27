class Datapool:
    def __init__(self):
        self.pool = {}

    def get(self, key):
        return self.pool.get(key)

    def set(self, key, value):
        self.pool[key] = value
