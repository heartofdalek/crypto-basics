from enc.method.base import Base as BaseMethod

class CaesarBase(BaseMethod):

    def load(self, options):
        
        super().load(options)
        
        self.key = int(self.key)
        
        max_key_len = self.src_chars_len//2
        
        if self.key<0 or self.key>max_key_len:
            raise Exception(f'Key should be in range of 0-{max_key_len}')
        
    def before_load(self):
        pass
        
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
