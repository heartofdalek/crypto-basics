from enc.strategy.base import Base as BaseStrategy

class Substitute(BaseStrategy):

    def load(self, key, mapping):
        self.key = int(key)
    
    def decode(self, payload):
        print("decode(payload): define me")
    
    def encode(self, payload):
        print("encode(payload): define me")
