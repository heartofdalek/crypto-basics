from enc.method.base_mapper import BaseMapper


class CaesarBase(BaseMapper):

    def after_load(self):
        
        super().after_load()
        
        self.key = int(self.key)

        ''' key shouldn't be more than half of an alphabet size '''
        max_key_len = self.src_chars_len//2

        if self.key < 0 or self.key > max_key_len:
            raise Exception(f'Key should be in range of 0-{max_key_len}')

    def decode(self, payload):

        payload = payload.upper()

        result = []

        for char in payload:
            ix = self.find_index(self.dst_map, char)
            subst_ix = self.find_decode_index(ix)
            result.append(self.src_chars[subst_ix])

        return ''.join(result)

    def encode(self, payload):

        payload = payload.upper()

        result = []

        for char in payload:
            ix = self.find_index(self.src_map, char)
            subst_ix = self.find_encode_index(ix)
            result.append(self.dst_chars[subst_ix])

        return ''.join(result)

    def find_encode_index(self, ix):
        return (ix + self.key) % self.dst_chars_len

    def find_decode_index(self, ix):
        return (ix + self.dst_chars_len - self.key) % self.dst_chars_len
