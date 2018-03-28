class Datapool:
    def __init__(self, **kwargs):
        self.pool = kwargs

    def get(self, key):
        return self.pool.get(key)

    def set(self, key, value):
        self.pool[key] = value
