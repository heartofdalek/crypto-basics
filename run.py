#!/usr/bin/python3

from argparse import ArgumentParser as OptionParser
from enc.sf import EncryptStrategy

sf = EncryptStrategy()
allowed_strategies = sf.allowed_strategies.keys()

parser = OptionParser(description='Make symmetric encryption with some basic algo\'s')

parser.add_argument("-k", "--key", dest="key", default="8", help="encryption key")
parser.add_argument("-m", "--map", dest="mapping", default="mapping_orig.txt", help="char mapping file")
parser.add_argument("-s", "--strategy", dest="strategy", default="caesar_simple", help="encryption strategy method: {}".format(", ".join(allowed_strategies)))
parser.add_argument("-t", "--type", dest="type", default="encode", help="encryption direction: encode, decode")
parser.add_argument("-d", "--debug", dest="is_debug", action='store_true', default=False, help="enable debug if specified")
parser.add_argument("payload", type=str, nargs='?', default="", help="text to encode/decode")

options = parser.parse_args()

payload = options.payload if len(options.payload) else ""

try:
    
    strategy = sf.create(options.strategy)
    strategy.load(options)
    
    result = strategy.call(options, payload)
    
    print(result)
    
except Exception as e:
    print(f'\n]> Error: {e}\n')
    parser.print_help()
