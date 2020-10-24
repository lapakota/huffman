class TextCommands:
    @staticmethod
    def check_empty_file(data):
        if not data:
            print("File is empty")
            exit(0)

    @staticmethod
    def print_final_message(command, path):
        print(f"{command} was finished\nFile: {path}")

    @staticmethod
    def print_message_with_exit(message):
        print(message)
        exit(0)
