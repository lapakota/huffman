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
        output_path = ''
        try:
            with open(self.path, 'rb') as file:
                file_data = pickle.load(file)
                decode_info = pickle.load(file)
                self.decode_huff_map = decode_info[0]
                self.filename = decode_info[1]
                self.file_extension = decode_info[2]
                self.hash = decode_info[3]
                self.is_bin = decode_info[4]
                access_time = decode_info[5]
                modify_time = decode_info[6]
                mode = 'w' if not self.is_bin else 'wb'

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
        except Exception as e:
            TextCommands.print_message_with_exit(e)

        TextCommands.print_final_message('Decoding', output_path)
        self.check_integrity(decoded_text)

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
        if self.hash == hashlib.md5(decoded_text).hexdigest() if self.is_bin \
                else hashlib.md5(decoded_text.encode('utf-8')).hexdigest():
            print("Integrity in normal state")
        else:
            print("Some errors with integrity")
