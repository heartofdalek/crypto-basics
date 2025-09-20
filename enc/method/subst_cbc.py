from enc.method.base import Base as BaseMethod

class SubstCBC(BaseMethod):
    
    def before_load(self):
        pass
    
    def after_load(self):
        
        min_key_length = 6
        
        self.key = list(str(self.key).upper())
        
        if self.key_len<min_key_length:
            raise Exception(f'Key MUST be length of {min_key_length} or more')
        
        self.src_map = {}
        self.dst_map = {}
        self.new_dst_chars = []
        
        for ix in range(self.src_chars_len):
            if self.dst_chars[ix] not in self.dst_map:
                self.src_map[self.src_chars[ix]] = (self.dst_chars[ix], ix)
                self.dst_map[self.dst_chars[ix]] = (self.src_chars[ix], ix)
                self.new_dst_chars.append(self.dst_chars[ix])
            else:
                self.src_map[self.src_chars[ix]] = (self.src_chars[ix], ix)
                self.dst_map[self.src_chars[ix]] = (self.src_chars[ix], ix)
                self.new_dst_chars.append(self.src_chars[ix])
        
        self.dst_chars = self.new_dst_chars
        self.dst_char_len = len(self.dst_chars)
        
        self.base_shift = self.calc_base_shift(self.key)
        
        self.block_len = self.key_len
        
        self.block_pad_char = ' '
                
    def calc_base_shift(self, key):
        
        weight = 1
        shift = 0

        for x in key:
            idx = ord(x)
            shift += idx*weight
            weight = weight + 1 if weight<10 else 1
            
        shift = shift % self.dst_chars_len

        return shift

    def encode(self, payload):
        
        payload = str(payload).upper()
        
        result = []
        
        last_block = self.key
        current_block = []
        
        for ix in range(len(payload)):
            
            if ix>0 and ix % self.block_len == 0:
                last_block = current_block
                current_block = []
            
            char = self.src_map[payload[ix]][0]
            block_char = self.src_map[last_block[ ix % self.block_len ]][0]
            
            char_idx = self.find_index(self.dst_map, char)
            key_idx = self.find_index(self.dst_map, block_char)
            
            encoded_char_idx = (char_idx + key_idx + self.base_shift) % self.dst_char_len
            
            current_block.append( self.dst_chars[encoded_char_idx] )
            result.append( self.dst_chars[encoded_char_idx] )
        
        return ''.join(result)
    
    def decode(self, payload):
        
        payload = str(payload).upper()
        
        result = []
        
        last_block = self.key
        current_block = []
        
        for ix in range(len(payload)):
            
            if ix>0 and ix % self.block_len == 0:
                last_block = current_block
                current_block = []
            
            char = payload[ix]
            block_char = self.src_map[last_block[ ix % self.block_len ]][0]
            
            char_idx = self.find_index(self.dst_map, char)
            key_idx = self.find_index(self.dst_map, block_char)
            
            decoded_char_idx = (char_idx - key_idx - self.base_shift) % self.dst_char_len
            
            current_block.append( char )
            result.append( self.dst_map[self.dst_chars[decoded_char_idx]][0] )
        
        return ''.join(result)

    def find_index(self, chars, char):
        if char in chars:
            return chars[char][1]
        else:
            raise Exception(f'Char {char} not in {self.dst_chars}')
