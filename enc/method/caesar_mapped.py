from enc.method.caesar_base import CaesarBase

class CaesarMapped(CaesarBase):

    def after_load(self):
        if set(self.src_chars) != set(self.dst_chars):
            print("")
            print(list(sorted(self.src_chars)))
            print(list(sorted(self.dst_chars)))
            raise Exception("Character mapping contains different character set. Possible collision on decode. Exiting.")
