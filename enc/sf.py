from enc.strategy.base import Base as BaseStrategy

class EncryptStrategy():
    
    allowed_strategies = {
        'caesar' : 'Caesar'
    }
    
    def __init(self):
        pass
    
    def create(self, strategy) -> BaseStrategy:
        
        if strategy not in self.allowed_strategies:
            raise Exception("Wrong encryption strategy method. Available: {}".format(", ".join(self.allowed_strategies.keys())))
            
        classname = self.allowed_strategies[strategy]
        module = __import__(f'enc.strategy.{strategy}', globals(), locals(), [classname], 0)
        callable_name = getattr(module, classname)
        return callable_name()
