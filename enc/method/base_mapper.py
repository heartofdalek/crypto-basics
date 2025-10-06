from enc.method.base import Base as BaseMethod


class BaseMapper(BaseMethod):

    def load(self):
        ''' does initial work to setup working environment '''

        self.before_load()

        self.key = self.options.key
        self.key_len = len(self.key)

        self.after_load()


    def after_load(self):
        self.create_chars_list()
        self.build_chars_map()


    def build_chars_map(self):
        ''' creates charaters mapping to simplify indexes and chars search during substitution '''

        self.src_map = {}
        self.dst_map = {}
        self.new_dst_chars = []

        replace_origin_dst_chars = False

        for ix in range(self.src_chars_len):
            if 0 <= ix < self.dst_chars_len and self.dst_chars[ix] not in self.dst_map:
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


    def decode(self, payload):
        ''' abstract method but not @abstract '''
        pass


    def encode(self, payload):
        ''' abstract method but not @abstract '''
        pass

 
