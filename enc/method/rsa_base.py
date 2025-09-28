from enc.method.base import Base as BaseMethod
from argparse import ArgumentParser as OptionParser
from math import gcd
import os, sys

class RSABase(BaseMethod):
    
    def before_load(self):
        self.options_parser.add_argument("-o", "--output-file-name", dest="output_file_name", default="id_rsa", help="template name for private and public keys")
        self.options = self.options_parser.parse_args()
        self.generate_priv_file = "{}.priv".format(self.options.output_file_name)
        self.generate_pub_file = "{}.pub".format(self.options.output_file_name)
        
    def after_load(self):
        self.key_file = self.key if self.key!='8' else None

    def keygen(self, payload):
        p = self.generate_p()
        q = self.generate_q(p)
        
        if not self.are_coprime(p, q):
            raise Exception("p and q are not coprime!")
        
        n = p * q
        phi = (p - 1) * (q - 1)
            
        e = 2  # start with minimal value
        while e < phi:
            if self.are_coprime(e, phi):
                break
            e += 1
        
        if e >= phi:
            raise Exception("Couldn't find coprime e with phi!")

        d = self.find_d(e, phi)
        
        if d is None:
            raise Exception("Couldn't find d!")

        if self.options.is_debug:
            print(p, q, n, phi, e, d)
        
        if os.path.exists(self.generate_priv_file) and not self.options.answer_yes:
            
            answer = 'n'
            
            while True:
                answer = input("Private key exists! Create another one? (у/N): ").lower().strip()
                if answer=='y':
                    break
                elif answer=='n' or answer=='':
                    sys.exit()

        with open(self.generate_priv_file, "w") as f:
            f.write(f"{d},{p},{q}")
            
        with open(self.generate_pub_file, "w") as f:
            f.write(f"{e},{n}")
            
        return "Public and private keys created"

    def encode(self, payload):
        
        key_file = self.key_file if self.key_file is not None else self.generate_pub_file
        
        e, n = self.read_key(key_file)
        
        result = []
        
        for char in payload:
            C = pow(ord(char), e, n)
            result.append(C)

        return ','.join(map(str,result))
    
    def decode(self, payload):
        
        key_file =  self.key_file if self.key_file is not None else self.generate_priv_file
        
        d, p, q = self.read_key(key_file)
        
        n = p * q
        
        result = []
        
        for char in payload.split(','):
            char_int = int(char)
            C = pow(char_int, d, n)
            result.append(chr(C))
        
        return ''.join(result)
 
    def generate_p(self):
        return 241
    
    # numbers should be different, so p as arg to ckeck if need
    # generator should
    def generate_q(self, p):
        return 307
    
    # a and b are comprime when they have greatest mutual divisor as 1
    def are_coprime(self, a, b):
        return gcd(a, b) == 1

    def find_d(self, e, phi):
        for d in range(1, phi):
            if (e * d) % phi == 1:
                return d
        return None

    def read_key(self, filename):
        result = []
        
        with open(filename, 'r') as f:
            txt = f.read().strip().split(',')
            for c in txt:
                result.append(int(c))

        return result
 
    def create_chars_list(self):
        pass
    
    def build_chars_map(self):
        pass
