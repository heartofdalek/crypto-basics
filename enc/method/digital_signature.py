import random
import os
import sys
from sympy import isprime, nextprime
from enc.method.base import Base as BaseMethod


class DigitalSignature(BaseMethod):

    error_message = 'Sign incorrect'
    success_message = 'Verified'
        
    def keygen(self, *args):
        ''' generate all necessary data for private and public keys '''
        
        # recreate keys if needs
        if os.path.exists(self.generate_priv_file) and not self.options.answer_yes:

            answer = 'n'

            while True:
                answer = input(
                    "Private key exists! Create another one? (у/N): ").lower().strip()
                if answer == 'y':
                    break
                elif answer == 'n' or answer == '':
                    sys.exit()
        '''
        Параметры системы ЭП - числа p, q, a. Эти числа не являются секретными.
        Конкретный набор их значений может быть общим для группы пользователей.
        '''
        param_p, param_q, param_a = self.generate_parameters()

        priv_key_x = random.randint(2, param_q - 1)
        pub_key_y = pow(param_a, priv_key_x, param_p)

        ''' write private key file
        Секретный ключ - числа p, q, a и x
        '''
        with open(self.generate_priv_file, "w") as f:
            f.write(f"{param_p},{param_q},{param_a},{priv_key_x}")

        ''' write public key file
        Открытым ключом являются числа p, q, a и y
        '''
        with open(self.generate_pub_file, "w") as f:
            f.write(f"{param_p},{param_q},{param_a},{pub_key_y}")

    def generate_parameters(self):
        
        p_bits = random.randint(510, 511) # 2^509<p<2^512
        q_bits = 255 # 2^254<q<2^256
        
        param_q = self.generate_prime(q_bits)
        
        while True:
            
            n = random.randint(2**(p_bits-1)//param_q, 2**p_bits//param_q)
            candidate = n * param_q + 1
            
            if isprime(candidate) and 2**509 < candidate < 2**512:
                param_p = candidate
                break


        # Генерация a: a^q mod p = 1
        
        h = (param_p - 1) // param_q
        
        while True:
            # Берем случайное g в диапазоне [2, p-2]
            g = random.randint(2, param_p - 2)
        
            # Вычисляем a = g^h mod p
            param_a = pow(g, h, param_p)
        
            # Проверяем, что a != 1, это гарантирует, что a^q ≡ 1 mod p
            if param_a != 1:
                break
        
        return (param_p, param_q, param_a)

    def generate_prime(self, bits):
        ''' generate prime number with size of {bits} '''
        
        result = 0
        
        while True:
            candidate = random.getrandbits(bits)
            
            candidate |= (1 << bits - 1) | 1  # setup high and low bits
            
            if isprime(candidate):
                return candidate

    def sign(self, payload):
        ''' creates digital sign of input payload '''
        
        # чтение файла приватного ключа
        key_file = self.key_file if self.key_file is not None else self.generate_priv_file
        
        param_p, param_q, param_a, priv_key_x = self.read_key(key_file)
        
        # хеш входной строки
        hm = self.hash(payload)
        
        if hm % param_q == 0:
            hm = 1
        
        '''
        Вычисляем подпись с рандомизированным k = 1<k<q
        Значения r1, s являются электронной подписью сообщения payload и передаются вместе с ним по каналам связи.
        '''
        while True:
            k = random.randint(2, param_q-1)
            r = pow(param_a, k, param_p)
            r1 = r % param_q
            
            if r1 == 0:
                continue
                
            s = ( priv_key_x*r1 + k * hm ) % param_q
            
            if s != 0:
                break

        return f'{payload}|{r1},{s}'
    
    def verify(self, payload):
        ''' checks digital sign of a payload '''
        
        # чтение файла публичного ключа м последующим разбором на переменные
        key_file = self.key_file if self.key_file is not None else self.generate_pub_file
        
        param_p, param_q, param_a, pub_key_y = self.read_key(key_file)
        
        delim_pos = payload.rfind("|")
        
        m = payload[0:delim_pos]
        r1, s = list(map(int, payload[delim_pos+1:].split(",")))

        if not (0<r1<param_q and 0<s<param_q):
            return self.error_message
        
        # хеш входной строки
        hm = self.hash(m)
        
        if hm % param_q == 0:
            hm = 1
    
        # Вычисление параметров согласно алгоритму
        v = pow(hm, param_q - 2, param_q)
        
        z1 = (s * v) % param_q
        z2 = ((param_q - r1) * v) % param_q
        
        u = (pow(param_a, z1, param_p) * pow(pub_key_y, z2, param_p)) % param_p
        u = u % param_q
        
        return self.success_message if u == r1 else self.error_message
        
    
    def hash(self, payload):
        
        result = 0
        divider = 2**16
        
        for char in payload:
            result = (result + ord(char)) % divider
        
        return result % divider

    ''' служебные методы  '''

    def before_load(self):
        self.options_parser.add_argument("-o", "--output-file-name", dest="output_file_name",
                                         default="ds", help="template name for private and public keys")
        self.options = self.options_parser.parse_args()
        self.generate_priv_file = "{}.priv".format(
            self.options.output_file_name)
        self.generate_pub_file = "{}.pub".format(self.options.output_file_name)

    def after_load(self):
        self.key_file = self.key if self.key != '8' else None

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
