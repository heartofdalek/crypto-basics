#!/usr/bin/python3

from optparse import OptionParser
from enc.sf import EncryptStrategy

parser = OptionParser()
parser.add_option("-k", "--key", dest="key", default="8", help="encryption key")
parser.add_option("-m", "--map", dest="mapping", default="mapping_orig.txt", help="char mapping file")
parser.add_option("-s", "--strategy", dest="strategy", default="caesar_simple", help="encryption strategy method")
parser.add_option("-t", "--type", dest="type", default="encode", help="encryption direction: encode or decode")

(options, args) = parser.parse_args()

payload = args[0] if len(args) else ""

try:
    
    strategy = EncryptStrategy().create(options.strategy)
    strategy.load(options.key, options.mapping)
    
    result = strategy.call(options.type, payload)
    
    print(result)
    
except Exception as e:
    print(f'\n]> Error: {e}\n')
    parser.print_help()
