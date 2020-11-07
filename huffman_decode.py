import hashlib
import os
import pickle

from text_commands import TextCommands


class HuffmanDecoding:
    def __init__(self, path):
        self.path = path
        self.nodes_heap = []
        self.decode_huff_map = 0
        self.filename = 0
        self.file_extension = 0
        self.hash = 0
        self.is_bin = False

    def decode_file(self):
        try:
            with open(self.path, 'rb') as file:
                file_data, \
                self.decode_huff_map, self.filename, self.file_extension, \
                self.hash, self.is_bin, access_time, modify_time, mode \
                    = self.load_data(file)

                bit_string = ""
                for byte in file_data:
                    # перевод в бинарный вид и добивание нулями слева до длины байта
                    bits = bin(byte)[2:].rjust(8, '0')
                    bit_string += bits
                encoded_text = self.remove_extras(bit_string)
                decoded_text = self.decode_data(encoded_text)

            output_path = self.filename + "_decoded" + self.file_extension

            with open(output_path, mode) as output:
                output.write(decoded_text)
            # Меняем таймштампы
            os.utime(output_path, (access_time, modify_time))
            TextCommands.print_final_message('Decoding', output_path)
            self.check_integrity(decoded_text)
        except Exception as e:
            TextCommands.print_message_with_exit(e)

    @staticmethod
    def load_data(file):
        file_data = pickle.load(file)
        decode_info = pickle.load(file)
        return file_data, \
               decode_info[0], decode_info[1], decode_info[2], \
               decode_info[3], decode_info[4], decode_info[5], decode_info[6], \
               'w' if not decode_info[4] else 'wb'

    @staticmethod
    def remove_extras(extra_encoded_text):
        # берём первые 8 по ним смотрим излишние, убираем эти 8 и с конца обрезаем лишнее
        extra_bits = extra_encoded_text[:8]
        extra_bits_count = int(extra_bits, 2)
        extra_encoded_text = extra_encoded_text[8:]
        encoded_text = extra_encoded_text[:-extra_bits_count]
        return encoded_text

    def decode_data(self, encoded_text):
        current_code = ""
        decoded_text = bytearray() if self.is_bin else ''
        for bit in encoded_text:
            current_code += bit
            if current_code in self.decode_huff_map:
                character = self.decode_huff_map[current_code]
                if self.is_bin:
                    decoded_text.append(character)
                else:
                    decoded_text += character
                current_code = ""
        return decoded_text

    def check_integrity(self, decoded_text):
        if self.hash == hashlib.md5(decoded_text if self.is_bin
                                    else decoded_text.encode('utf-8')).hexdigest():
            print("Integrity in normal state")
        else:
            print("Some errors with integrity")
