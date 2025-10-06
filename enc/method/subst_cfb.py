from enc.method.base_mapper import BaseMapper


class SubstCFB(BaseMapper):

    def after_load(self):
        
        super().after_load()
        
        min_key_length = 6

        self.key = list(str(self.key).upper())

        if self.key_len < min_key_length:
            raise Exception(f'Key MUST be length of {min_key_length} or more')

        self.base_shift = self.calc_base_shift(self.key)

        self.block_len = self.key_len

    def calc_base_shift(self, key):

        weight = 1
        shift = 0

        for x in key:
            char = self.src_map[x][0]
            idx = self.find_index(self.dst_map, char)
            shift += idx*weight
            weight = weight + 1 if weight < 10 else 1

        shift = shift % self.dst_chars_len

        return shift

    def action_encode(self, payload):

        payload = payload.upper()

        result = []

        last_block = self.key
        current_block = []

        for ix in range(len(payload)):

            if ix > 0 and ix % self.block_len == 0:
                last_block = current_block
                current_block = []

            char = self.src_map[payload[ix]][0]
            block_char = self.src_map[last_block[ix % self.block_len]][0]

            char_idx = self.find_index(self.dst_map, char)
            key_idx = self.find_index(self.dst_map, block_char)

            encoded_char_idx = (char_idx + key_idx +
                                self.base_shift) % self.dst_chars_len

            current_block.append(self.dst_chars[encoded_char_idx])
            result.append(self.dst_chars[encoded_char_idx])

        return ''.join(result)

    def action_decode(self, payload):

        payload = payload.upper()

        result = []

        last_block = self.key
        current_block = []

        for ix in range(len(payload)):

            if ix > 0 and ix % self.block_len == 0:
                last_block = current_block
                current_block = []

            char = payload[ix]
            block_char = self.src_map[last_block[ix % self.block_len]][0]

            char_idx = self.find_index(self.dst_map, char)
            key_idx = self.find_index(self.dst_map, block_char)

            decoded_char_idx = (char_idx - key_idx -
                                self.base_shift) % self.dst_chars_len

            current_block.append(char)
            result.append(self.dst_map[self.dst_chars[decoded_char_idx]][0])

        return ''.join(result)
