import os

from huffman_decode import HuffmanDecoding


class DirectoryDecoding:
    def __init__(self, path):
        self.path = path

    def decode_files(self):
        names = os.listdir(self.path)
        for name in names:
            fullname = os.path.join(self.path, name)
            if os.path.isfile(fullname):
                if os.path.splitext(name)[1] == '.huf':
                    try:
                        h = HuffmanDecoding(fullname)
                        h.decode_file()
                        os.remove(fullname)
                    except Exception as e:
                        print(f"Trouble with file: {fullname}", e)
