import sys
import argparse

from huffman_encode import HuffmanEncoding
from huffman_decode import HuffmanDecoding


def parse_args(args):
    parser = argparse.ArgumentParser(description='Huffman encode/decode')
    parser.add_argument('--encode', dest='encode',
                        help='Input filename',
                        required=False)
    parser.add_argument('--decode', dest='decode',
                        help='Input filename',
                        required=False)
    parser.add_argument('--file', dest='help_file',
                        help='Input help file',
                        required=False)
    return parser.parse_args(args)


def args_handler():
    args = parse_args(sys.argv[1:])
    if args.encode:
        path = args.encode
        h = HuffmanEncoding(path)
        h.encode_file()
    elif args.decode:
        path = args.decode
        help_path = args.help_file
        h = HuffmanDecoding(path, help_path)
        h.decode_file()


def main():
    args_handler()


if __name__ == '__main__':
    main()
