from enc.method.base import Base as BaseMethod

class CaesarMapped(BaseMethod):

    lines = []

    def load(self, options):
        
        super().load(options)
        
        if set(self.src_chars) != set(self.dst_chars):
            print("")
            print(list(sorted(self.src_chars)))
            print(list(sorted(self.dst_chars)))
            raise Exception("Character mapping contains different character set. Possible collision!")
        
    def find_index(self, chars, char):
        return chars.index(char)

    def find_encode_index(self, ix):
        return ( ix + self.key ) % self.dst_chars_len
    
    def find_decode_index(self, ix):
        return ( ix + self.dst_chars_len - self.key ) % self.dst_chars_len

    def decode(self, payload):
        payload = list(payload.upper())
        plen = len(payload)
        
        if plen == 0:
            raise Exception("Payload is empty. Nothing to decode")
        
        result = []
        
        for char in payload:
            ix = self.find_index(self.dst_chars, char)
            subst_ix = self.find_decode_index(ix)
            result.append(self.src_chars[subst_ix])
        
        return ''.join(result)
    
    def encode(self, payload):
        payload = list(payload.upper())
        plen = len(payload)
        
        if plen == 0:
            raise Exception("Payload is empty. Nothing to encode")
        
        result = []
        
        for char in payload:
            ix = self.find_index(self.src_chars, char)
            subst_ix = self.find_encode_index(ix)
            result.append(self.dst_chars[subst_ix])
        
        return ''.join(result)
