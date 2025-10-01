class Base():

    def load(self, options, options_parser):
        ''' does initial work to setup working environment '''
        
        self.options = options
        self.options_parser = options_parser
        
        self.before_load()
        
        self.key = self.options.key
        self.key_len = len(self.key)
        
        self.create_chars_list()
        
        self.build_chars_map()
        
        self.after_load()

    def build_chars_map(self):
        ''' creates charaters mapping to simplify indexes and chars search during substitution '''
        
        self.src_map = {}
        self.dst_map = {}
        self.new_dst_chars = []
        
        replace_origin_dst_chars = False
        
        for ix in range(self.src_chars_len):
            if 0<=ix<self.dst_chars_len and self.dst_chars[ix] not in self.dst_map:
                self.src_map[self.src_chars[ix]] = (self.dst_chars[ix], ix)
                self.dst_map[self.dst_chars[ix]] = (self.src_chars[ix], ix)
                
                ''' used to fix char duplicates in substitution character sets '''
                self.new_dst_chars.append(self.dst_chars[ix])
            else:
                self.src_map[self.src_chars[ix]] = (self.src_chars[ix], ix)
                self.dst_map[self.src_chars[ix]] = (self.src_chars[ix], ix)
                
                ''' used to fix char duplicates in substitution character sets '''
                self.new_dst_chars.append(self.src_chars[ix])
                replace_origin_dst_chars = True
        
        ''' catched when we've got duplicates in dst_chars or it was shorter or empty '''
        if replace_origin_dst_chars:
            self.dst_chars = self.new_dst_chars
            self.dst_chars_len = len(self.dst_chars)
    
    def create_chars_list(self):
        ''' creates source and substitution charasters list, from a file in base but depends on implementation '''
        
        with open(self.options.mapping) as file:
            lines = [line.rstrip("\n") for line in file]
            
        self.src_chars = list(lines[0])
        self.dst_chars = list(lines[1])
        self.src_chars_len = len(self.src_chars)
        self.dst_chars_len = len(self.dst_chars)
        
        if self.src_chars_len == 0:
            raise Exception('Main character set shouldn\'t be empty!')
    
    def find_index(self, chars, char):
        if char in chars:
            return chars[char][1]
        else:
            raise Exception(f'Char {char} not in {self.dst_chars}')
    
    def before_load(self):
        ''' abstract method but not @abstract '''
        pass
        
    def after_load(self):
        ''' abstract method but not @abstract '''
        pass
        
    def decode(self, payload):
        ''' abstract method but not @abstract '''
        pass
    
    def encode(self, payload):
        ''' abstract method but not @abstract '''
        pass
        
    def call(self, payload):
        ''' entrypoint to make cli methods to work '''
        
        method = self.options.type
        
        callable_name = getattr(self, method, None)
        
        if callable_name is not None:
            return callable_name(payload)
        else:
            raise Exception(f'Wrong method: {method}')
