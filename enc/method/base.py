class Base():

    def load(self, options):
        
        self.options = options
        
        self.before_load()
        
        self.key = options.key
        self.key_len = len(self.key)
        
        with open(options.mapping) as file:
            lines = [line.rstrip("\n") for line in file]
            
        self.src_chars = list(lines[0])
        self.dst_chars = list(lines[1])
        self.src_chars_len = len(self.src_chars)
        self.dst_chars_len = len(self.dst_chars)
        
        if self.src_chars_len == 0:
            raise Exception('Main character set shouldn\'t be empty!')
        
        self.src_map = {}
        self.dst_map = {}
        self.new_dst_chars = []
        
        replace_origin_dst_chars = False
        
        for ix in range(self.src_chars_len):
            if 0<=ix<self.dst_chars_len and self.dst_chars[ix] not in self.dst_map:
                self.src_map[self.src_chars[ix]] = (self.dst_chars[ix], ix)
                self.dst_map[self.dst_chars[ix]] = (self.src_chars[ix], ix)
                self.new_dst_chars.append(self.dst_chars[ix])
            else:
                self.src_map[self.src_chars[ix]] = (self.src_chars[ix], ix)
                self.dst_map[self.src_chars[ix]] = (self.src_chars[ix], ix)
                self.new_dst_chars.append(self.src_chars[ix])
                replace_origin_dst_chars = True
        
        # because we've got duplicates in dst_chars or it was shorter or empty
        if replace_origin_dst_chars:
            self.dst_chars = self.new_dst_chars
            self.dst_char_len = len(self.dst_chars)
        
        self.after_load()
    
    def find_index(self, chars, char):
        if char in chars:
            return chars[char][1]
        else:
            raise Exception(f'Char {char} not in {self.dst_chars}')
    
    def before_load(self):
        print("before_load(): define me")
        
    def after_load(self):
        print("after_load(): define me")
        
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
