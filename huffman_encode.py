import heapq
import os
import pickle
import hashlib

from node import Node
from text_commands import TextCommands


class HuffmanEncoding:
    def __init__(self, path):
        self.path = path
        self.nodes_heap = []
        self.encode_huff_map = {}
        self.decode_huff_map = {}
        self.filename = ''
        self.file_extension = ''
        self.huff_extension = ".huf"
        self.hash = 0
        self.is_bin = False

    def encode_file(self):
        self.filename, self.file_extension, output_path, \
        self.is_bin, mode, access_time, modify_time \
            = self.load_data()
        self.check_huf_file()
        try:
            with open(self.path, mode) as file, open(output_path, 'wb') as output:
                text = file.read()
                self.hash = hashlib.md5(text if self.is_bin
                                        else text.encode('utf-8')).hexdigest()
                frequency = self.make_frequency_dict(text)
                self.make_heap(frequency)
                self.merge_nodes()
                self.create_codes_map()

                encoded_text = ''.join([self.encode_huff_map[c] for c in text])
                # дополненный текст
                extra_encoded_text = self.format_encoded_text(encoded_text)
                b = self.get_byte_array(extra_encoded_text)

                pickle.dump(bytes(b), output)
                pickle.dump((self.decode_huff_map,
                             self.filename,
                             self.file_extension,
                             self.hash,
                             self.is_bin,
                             access_time,
                             modify_time),
                            output)
                TextCommands.print_final_message('Encoding', output_path)
        except Exception as e:
            TextCommands.print_message_with_exit(e)

    def check_huf_file(self):
        if self.file_extension == self.huff_extension:
            TextCommands.print_message_with_exit("Can't compress already compressed file")

    def load_data(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + self.huff_extension
        is_bin = self.is_binary()
        mode = 'r' if not is_bin else 'rb'
        access_time = os.stat(self.path).st_atime
        modify_time = os.stat(self.path).st_mtime
        return filename, file_extension, output_path, \
               is_bin, mode, access_time, modify_time

    def is_binary(self):
        try:
            with open(self.path, 'tr') as check_file:
                check_file.read()
                return False
        except UnicodeDecodeError:
            return True

    @staticmethod
    def make_frequency_dict(text):
        frequency = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    @staticmethod
    def format_encoded_text(encoded_text):
        extra_bits_count = 8 - len(encoded_text) % 8
        for i in range(extra_bits_count):
            encoded_text += "0"
        # переводит число в двоичный вид и добивает слева нулями
        bin_extra_bit_count = "{0:08b}".format(extra_bits_count)
        encoded_text = bin_extra_bit_count + encoded_text
        return encoded_text

    @staticmethod
    def get_byte_array(extra_encoded_text):
        if len(extra_encoded_text) % 8 != 0:
            print("Error with data")
            exit(0)
        b = bytearray()
        for i in range(0, len(extra_encoded_text), 8):
            byte = extra_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def make_heap(self, frequency):
        for key in frequency:
            node = Node(key, frequency[key])
            heapq.heappush(self.nodes_heap, node)

    def merge_nodes(self):
        while len(self.nodes_heap) > 1:
            node1 = heapq.heappop(self.nodes_heap)
            node2 = heapq.heappop(self.nodes_heap)

            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.nodes_heap, merged)

    def create_codes_map(self):
        root = heapq.heappop(self.nodes_heap)
        current_code = ""
        self.create_codes_recursively(root, current_code)

    def create_codes_recursively(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.encode_huff_map[root.char] = current_code
            self.decode_huff_map[current_code] = root.char
            return

        self.create_codes_recursively(root.left, current_code + "0")
        self.create_codes_recursively(root.right, current_code + "1")
