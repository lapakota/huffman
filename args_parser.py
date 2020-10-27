import argparse
import sys

from huffman_decode import HuffmanDecoding
from huffman_encode import HuffmanEncoding
from huffman_decode_directory import DirectoryDecoding
from huffman_encode_directory import DirectoryEncoding


class ArgsParser:
    @staticmethod
    def parse_args(args):
        parser = argparse.ArgumentParser(description='Huffman encode/decode')
        parser.add_argument('--encode', dest='encode',
                            help='Input file name to encode',
                            required=False)
        parser.add_argument('--decode', dest='decode',
                            help='Input file name to decode',
                            required=False)
        parser.add_argument('--encode_dir', dest='enc_directory',
                            help='Input directory name to encode',
                            required=False)
        parser.add_argument('--decode_dir', dest='dec_directory',
                            help='Input directory name to decode',
                            required=False)
        return parser.parse_args(args)

    def args_handler(self):
        args = self.parse_args(sys.argv[1:])
        if args.encode:
            path = args.encode
            h = HuffmanEncoding(path)
            h.encode_file()
        elif args.decode:
            path = args.decode
            h = HuffmanDecoding(path)
            h.decode_file()
        if args.enc_directory:
            path = args.enc_directory
            h = DirectoryEncoding(path)
            h.encode_files()
        elif args.dec_directory:
            path = args.dec_directory
            h = DirectoryDecoding(path)
            h.decode_files()
