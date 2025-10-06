class Base():

    def __init__(self, options_parser):
        self.options_parser = options_parser
        self.options = options_parser.parse_args()


    def load(self):
        ''' does initial work to setup working environment '''

        self.before_load()

        self.key = self.options.key
        self.key_len = len(self.key)

        self.after_load()


    def before_load(self):
        ''' abstract method but not @abstract '''
        pass


    def after_load(self):
        ''' abstract method but not @abstract '''
        pass


    def call(self, payload):
        ''' entrypoint to make cli methods to work '''

        method = self.options.type

        callable_name = getattr(self, method, None)

        if callable_name is not None:
            return callable_name(payload)
        else:
            raise Exception(f'Wrong method: {method}')
