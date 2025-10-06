import os
import sys
from math import gcd
from enc.method.base import Base as BaseMethod
from argparse import ArgumentParser as OptionParser


class RSABase(BaseMethod):

    def before_load(self):
        self.options_parser.add_argument("-o", "--output-file-name", dest="output_file_name",
                                         default="id_rsa", help="template name for private and public keys")
        self.options = self.options_parser.parse_args()
        self.generate_priv_file = "{}.priv".format(
            self.options.output_file_name)
        self.generate_pub_file = "{}.pub".format(self.options.output_file_name)

    def after_load(self):
        self.key_file = self.key if self.key != '8' else None

    def action_keygen(self, payload):
        ''' This method creates all necessary variables to implementing encoding and decoding:
        p, q, n, phi, d.
        Method calls from a cli to use decode/encode with different keys.
        '''

        # Выбирается два больших простых числа p и q.
        p = self.generate_p()
        q = self.generate_q(p)

        ''' This check should be in generate_q with while cycle but we have constants in task so check goes here according to the task:
        В программе предусмотреть проверку, являются ли два числа взаимно простыми.
        '''
        if not self.are_coprime(p, q):
            raise Exception("p and q are not coprime!")

        n = p * q
        phi = (p - 1) * (q - 1)

        ''' start with minimal possible value
        Выбирается минимально возможное число e, которое взаимно простое с результатом phi=(p-1)*(q-1)
        '''
        e = 2
        while e < phi:
            if self.are_coprime(e, phi):
                break
            e += 1

        if e >= phi:
            raise Exception("Couldn't find coprime e with phi!")

        ''' Определяется такое число d, для которого является истинным соотношение (e*d)mod(phi)=1 '''
        d = self.find_d(e, phi)

        if d is None:
            raise Exception("Couldn't find d!")

        if self.options.is_debug:
            print(p, q, n, phi, e, d)

        ''' user decides should we recreate keys or not '''
        if os.path.exists(self.generate_priv_file) and not self.options.answer_yes:

            answer = 'n'

            while True:
                answer = input(
                    "Private key exists! Create another one? (у/N): ").lower().strip()
                if answer == 'y':
                    break
                elif answer == 'n' or answer == '':
                    sys.exit()

        ''' write private key file
        Секретный ключ - числа d, p и q
        '''
        with open(self.generate_priv_file, "w") as f:
            f.write(f"{d},{p},{q}")

        ''' write public key file
        Открытым ключом являются числа e и n 
        '''
        with open(self.generate_pub_file, "w") as f:
            f.write(f"{e},{n}")

        return "Public and private keys created"

    def action_encode(self, payload):
        ''' read public key from a file '''
        key_file = self.key_file if self.key_file is not None else self.generate_pub_file

        e, n = self.read_key(key_file)

        result = []

        for char in payload:
            C = pow(ord(char), e, n)
            result.append(C)

        return ','.join(map(str, result))

    def action_decode(self, payload):
        ''' read private key from a file '''
        key_file = self.key_file if self.key_file is not None else self.generate_priv_file

        d, p, q = self.read_key(key_file)

        ''' restore n from p and q '''
        n = p * q

        result = []

        for char in payload.split(','):
            char_int = int(char)
            C = pow(char_int, d, n)
            result.append(chr(C))

        return ''.join(result)

    def generate_p(self):
        return 241

    def generate_q(self, p):
        ''' numbers should be different, so p as arg to check coprime if needs '''
        return 307

    def are_coprime(self, a, b):
        ''' a and b are comprime when they have greatest mutual divisor as 1 '''
        return gcd(a, b) == 1

    def find_d(self, e, phi):
        for d in range(1, phi):
            if (e * d) % phi == 1:
                return d
        return None

    def read_key(self, filename):
        ''' read key from a file and prepare key structure '''

        result = []

        with open(filename, 'r') as f:
            txt = f.read().strip().split(',')
            for c in txt:
                result.append(int(c))

        return result

    def create_chars_list(self):
        ''' clear for future '''
        pass

    def build_chars_map(self):
        ''' clear for future '''
        pass
