import glob
import os
from enc.method.base import Base as BaseMethod


class EncryptMethod():

    allowed_methods = {}

    def __init__(self):
        self.load_allowed_methods()
        pass

    def load_allowed_methods(self):
        path = os.path.dirname(os.path.dirname(__file__))
        for file in glob.glob(f'{path}/config/*.py'):
            methods_config = os.path.splitext(os.path.basename(file))[0]
            
            cfg = 'allowed_methods'
            
            module = __import__(
                f'config.{methods_config}', globals(), locals(), [cfg], 0)
            
            allowed_methods = getattr(module, cfg)
            
            self.allowed_methods.update(allowed_methods)
            

    def create(self, method) -> BaseMethod:
        ''' fabric method to initialize one of the allowed encrypt methods '''

        if method not in self.allowed_methods:
            raise Exception("Wrong encryption method method. Available: {}".format(
                ", ".join(self.allowed_methods.keys())))

        classname = self.allowed_methods[method]
        module = __import__(
            f'enc.method.{method}', globals(), locals(), [classname], 0)
        callable_name = getattr(module, classname)
        return callable_name()
