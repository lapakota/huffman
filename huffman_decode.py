import hashlib
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

                bit_string = ""

                for byte in file_data:
                    # перевод в бинарный вид и добивание нулями слева до длины байта
                    bits = bin(byte)[2:].rjust(8, '0')
                    bit_string += bits

                encoded_text = self.remove_extras(bit_string)
                decoded_text = self.decode_text(encoded_text)

            output_path = self.filename + "_decoded" + self.file_extension

            with open(output_path, 'w') as output:
                output.write(decoded_text)
        except Exception as e:
            TextCommands.print_message_with_exit(e)

        TextCommands.print_final_message('Decoding', output_path)

        if self.hash == hashlib.md5(decoded_text.encode('utf-8')).hexdigest():
            print("Integrity in normal state")
        else:
            print("Some errors with integrity")

    @staticmethod
    def remove_extras(extra_encoded_text):
        # берём первые 8 по ним смотрим излишние, убираем эти 8 и с конца обрезаем лишнее
        extra_bits = extra_encoded_text[:8]
        extra_bits_count = int(extra_bits, 2)
        extra_encoded_text = extra_encoded_text[8:]
        encoded_text = extra_encoded_text[:-extra_bits_count]
        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.decode_huff_map:
                character = self.decode_huff_map[current_code]
                decoded_text += character
                current_code = ""
        return decoded_text
