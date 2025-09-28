from enc.method.base import Base as BaseMethod

class EncryptMethod():
    
    allowed_methods = {
        'caesar_simple' : 'CaesarSimple',
        'caesar_mapped' : 'CaesarMapped',
        'subst_cfb' : 'SubstCFB',
        'bytes_cfb' : 'BytesCFB',
        'rsa_base' : 'RSABase'
    }
    
    def __init__(self):
        pass
    
    def create(self, method) -> BaseMethod:
        
        if method not in self.allowed_methods:
            raise Exception("Wrong encryption method method. Available: {}".format(", ".join(self.allowed_methods.keys())))
            
        classname = self.allowed_methods[method]
        module = __import__(f'enc.method.{method}', globals(), locals(), [classname], 0)
        callable_name = getattr(module, classname)
        return callable_name()
