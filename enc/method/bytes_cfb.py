import sys
from collections import deque
from enc.method.base import Base as BaseMethod


class BytesCFB(BaseMethod):

    bytes_mask = (
        0xff,
        0xffff,
        0xffffff,
        0xffffffff,
        0xffffffffff,
        0xffffffffffff,
        0xffffffffffffff,
        0xffffffffffffffff,
    )

    char_code_divisor = 256

    def after_load(self):

        min_key_length = 6

        self.key_stream = deque([])

        if self.key_len < min_key_length:
            raise Exception(f'Key MUST be length of {min_key_length} or more')

        self.initialize_key_stream(self.key)

    def detect_char_bytes_count(self, char_code):
        ''' detects number of bytes for one- and multi-byte char code to pack/unpack '''

        result = 0

        for mask in self.bytes_mask:
            if char_code & mask != char_code:
                result += 1
                continue
            result += 1
            break

        return result

    def pack(self, pack_list):
        ''' transform list of ints to  one- or multi-byte char '''

        bytes_num = len(pack_list)

        to_shift = 8 * (bytes_num - 1)

        result = 0

        for i in range(bytes_num):
            result = result | pack_list[i]
            result = result << to_shift
            to_shift -= 8

        return chr(result)

    def unpack(self, char):
        ''' transform one- or multi-byte char to list of ints '''

        char_code = ord(char)
        bytes_num = self.detect_char_bytes_count(char_code)

        to_shift = 8 * (bytes_num - 1)

        result = []

        for i in range(bytes_num-1, -1, -1):
            byte = char_code >> to_shift & self.bytes_mask[i]
            result.append(byte)
            to_shift -= 8

        return result

    def initialize_key_stream(self, key):
        ''' increase entropy to fix simple keys like AAAAAA and fill initial key stream '''

        weight = 1

        for x in key:

            bytes_list = self.unpack(x)

            for b in bytes_list:
                vector_b = (weight**3 + weight + b) % self.char_code_divisor
                self.key_stream.append(vector_b)
                weight = weight + 1 if weight < 20 else 1

    def action_encode(self, payload):

        result = []

        for char in payload:

            char_bytes = self.unpack(char)
            new_char = []

            for char_byte in char_bytes:

                key_byte = self.key_stream.popleft()
                encoded_char_byte = (
                    char_byte + key_byte) % self.char_code_divisor
                new_key_byte = (encoded_char_byte +
                                key_byte) % self.char_code_divisor

                self.key_stream.append(new_key_byte)
                new_char.append(encoded_char_byte)

            result.append(self.pack(new_char))

        return ''.join(result)

    def action_decode(self, payload):

        result = []

        for char in payload:

            char_bytes = self.unpack(char)
            new_char = []

            for char_byte in char_bytes:

                key_byte = self.key_stream.popleft()
                decoded_char_byte = (
                    char_byte - key_byte) % self.char_code_divisor
                new_key_byte = (char_byte + key_byte) % self.char_code_divisor

                self.key_stream.append(new_key_byte)
                new_char.append(decoded_char_byte)

            result.append(self.pack(new_char))

        return ''.join(result)

