#!/usr/bin/python3
import glob
import sys

sys.dont_write_bytecode = True

from enc.mf import EncryptMethod
from argparse import ArgumentParser



mf = EncryptMethod()
allowed_methods = list(mf.allowed_methods.keys())

mappings_available = []
for fl in glob.glob("mapping*.txt"):
    mappings_available.append(fl)

parser = ArgumentParser(
    description='Make crypto labs with some basic algo\'s')

parser.add_argument("-k", "--key", dest="key",
                    default="8", help="key or key file")
parser.add_argument("-m", "--map", dest="mapping", default="mapping.txt",
                    help="char mapping file: {}".format(", ".join(mappings_available)))
parser.add_argument("-s", "--method", dest="method", default=allowed_methods[0],
                    help="encryption method: {}".format(", ".join(allowed_methods)))
parser.add_argument("-t", "--type", dest="type", default="encode",
                    help="encryption direction: encode, decode")
parser.add_argument("-d", "--debug", dest="is_debug", action='store_true',
                    default=False, help="enable debug if specified")
parser.add_argument("-y", "--answer-yes", dest="answer_yes",
                    action='store_true', default=False, help="answer yes to any questions")
parser.add_argument("payload", type=str, nargs='?',
                    default="", help="text to encode/decode")

options = parser.parse_args()

payload = ''

if options.payload:
    payload = options.payload
elif not sys.stdin.isatty():
    payload = sys.stdin.read().strip()

try:

    method = mf.create(parser)
    method.load()

    result = method.call(payload)

    print(result)

except Exception as e:
    print(f']> Error: {e}')

    if options.is_debug:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    #parser.print_help()
