from enc.method.caesar_base import CaesarBase


class CaesarSimple(CaesarBase):

    def after_load(self):
        ''' make algo as classic caesar: source and substitute chars are identical '''

        super().after_load()

        self.dst_chars = self.src_chars
        self.dst_chars_len = self.src_chars_len
        self.dst_map = self.src_map
