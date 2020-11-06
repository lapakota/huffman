import unittest
from huffman_encode import *
from huffman_decode import *


class TestClassHuffmanEncoding(unittest.TestCase):
    huffman_text = HuffmanEncoding('test_data/test.ansi')
    huffman_bin = HuffmanEncoding('test_data/test.wav')

    def test_is_binary(self, huf_text=huffman_text, huf_bin=huffman_bin):
        self.assertFalse(huf_text.is_binary())
        self.assertTrue(huf_bin.is_binary())

    def test_make_frequency_dict(self, huf_text=huffman_text, huf_bin=huffman_bin):
        self.assertEqual(huf_text.make_frequency_dict('perpenbong'),
                         {'b': 1, 'e': 2, 'g': 1, 'n': 2, 'o': 1, 'p': 2, 'r': 1})
        self.assertEqual(huf_bin.make_frequency_dict(b'\xac\x00\x00\x10\xb1\x02'),
                         {0: 2, 2: 1, 16: 1, 172: 1, 177: 1})

    def test_format_encoded_text(self, huf_text=huffman_text):
        self.assertEqual(huf_text.format_encoded_text('1110010100'),
                         '000001101110010100000000')
        self.assertEqual(huf_text.format_encoded_text('1001111'),
                         '0000000110011110')
        self.assertEqual(huf_text.format_encoded_text('10011110'),
                         '000010001001111000000000')

    def test_get_byte_array(self, huf_text=huffman_text):
        self.assertEqual(huf_text.get_byte_array('1000101010100111'),
                         bytearray(b'\x8a\xa7'))
        with self.assertRaises(SystemExit) as cm:
            huf_text.get_byte_array('10001010101')
        self.assertEqual(str(cm.exception), '0')

    def test_create_codes_map(self):
        huf_text = HuffmanEncoding('test_data/test.ansi')
        huf_bin = HuffmanEncoding('test_data/test.wav')
        with open('test_data/test.ansi', 'r') as file_text, open('test_data/test.wav', 'rb') as file_bin:
            text = file_text.read()
            text_bin = file_bin.read()
        frequency_text = huf_text.make_frequency_dict(text)
        huf_text.make_heap(frequency_text)
        huf_text.merge_nodes()
        huf_text.create_codes_map()

        frequency_bin = huf_bin.make_frequency_dict(text_bin)
        huf_bin.make_heap(frequency_bin)
        huf_bin.merge_nodes()
        huf_bin.create_codes_map()
        self.assertEqual(list(huf_text.encode_huff_map.keys())[:15],
                         ['5', 'm', '[', '\x1b', '1', ' ', '0',
                          '2', '\n', '7', '9', '6', ';', '8', '4'])
        self.assertEqual(list(huf_bin.encode_huff_map.keys())[:15],
                         [253, 131, 136, 8, 119, 105, 137,
                          157, 122, 145, 89, 165, 146, 100, 97])


class TestClassHuffmanDecoding(unittest.TestCase):
    huffman_text = HuffmanDecoding('test_data/test_text.huf')
    huffman_bin = HuffmanDecoding('test_data/test_bin.huf')

    def test_remove_extras(self, huf_text=huffman_text):
        self.assertEqual(huf_text.remove_extras('1001010111000100'), '')
        self.assertEqual(huf_text.remove_extras('0000001110110000'), '10110')

    def test_decode_data(self):
        huf_text = HuffmanDecoding('test_data/test_text.huf')
        huf_text.is_bin = False

        huf_bin = HuffmanDecoding('test_data/test_bin.huf')
        huf_bin.is_bin = True

        with open('test_data/test_text.huf', 'rb') as file_text, \
                open('test_data/test_bin.huf', 'rb') as file_bin:
            text_file_data = pickle.load(file_text)
            text_decode_info = pickle.load(file_text)
            huf_text.decode_huff_map = text_decode_info[0]

            bin_file_data = pickle.load(file_bin)
            bin_decode_info = pickle.load(file_bin)
            huf_bin.decode_huff_map = bin_decode_info[0]

            bit_string = ""
            for byte in text_file_data:
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
            encoded_text = huf_text.remove_extras(bit_string)

            bit_string = ""
            for byte in bin_file_data:
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
            encoded_bin = huf_bin.remove_extras(bit_string)

        self.assertEqual(huf_text.decode_data(encoded_text)[:15],
                         '[48;5;0m[38;5')
        self.assertEqual(huf_bin.decode_data(encoded_bin)[:15],
                         bytearray(b'RIFFr\xac\x02\x00WAVEfmt'))


if __name__ == '__main__':
    unittest.main()
