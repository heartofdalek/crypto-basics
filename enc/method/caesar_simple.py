from enc.method.caesar_base import CaesarBase

class CaesarSimple(CaesarBase):
    
    def after_load(self):
        self.dst_chars = self.src_chars
        self.dst_chars_len = self.src_chars_len
