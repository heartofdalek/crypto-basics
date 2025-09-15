
class Base():
    
    def load(self, key, mapping):
        print("load(key, mapping): define me")
    
    def decode(self, payload):
        print("decode(payload): define me")
    
    def encode(self, payload):
        print("encode(payload): define me")
        
    def call(self, method, payload):
        if method == 'decode':
            return self.decode(payload)
        elif method == 'encode':
            return self.encode(payload)
        else:
            raise Exception("Wrong encryption direction. Available: encode, decode")
