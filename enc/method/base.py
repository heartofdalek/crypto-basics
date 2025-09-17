
class Base():
    
    lines = []
    
    def load(self, options):
        self.key = int(options.key)
        
        with open(options.mapping) as file:
            lines = [line.rstrip("\n") for line in file]
            
        self.src_chars = list(lines[0])
        self.dst_chars = list(lines[1])
        self.src_chars_len = len(self.src_chars)
        self.dst_chars_len = len(self.dst_chars)
        
        if self.src_chars_len != self.dst_chars_len or self.dst_chars_len == 0 or self.src_chars_len == 0:
            raise Exception("Character mapping lines is empty or charaster sets doesn't fit in length")
    
    def decode(self, payload):
        print("decode(payload): define me")
    
    def encode(self, payload):
        print("encode(payload): define me")
        
    def call(self, options, payload):
        
        method = options.type
        
        if method == 'decode':
            return self.decode(payload)
        elif method == 'encode':
            return self.encode(payload)
        else:
            raise Exception("Wrong encryption direction. Available: encode, decode")
