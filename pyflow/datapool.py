class Datapool:
    def __init__(self, init_data: dict):
        self.pool = init_data

    def get(self, key):
        return self.pool.get(key)

    def set(self, key, value):
        self.pool[key] = value
