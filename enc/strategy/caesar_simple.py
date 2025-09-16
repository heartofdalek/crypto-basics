from enc.strategy.base import Base as BaseStrategy

class CaesarSimple(BaseStrategy):
        
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
            ix = self.find_index(self.src_chars, char)
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
            result.append(self.src_chars[subst_ix])
        
        return ''.join(result) 
