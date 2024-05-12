import os
import hashlib

class NFile:

    # .local/share/nvim
    __ROOT_DIR = os.path.expanduser("~/.local/share/nvim/fnote-vim")

    def _create_root_dir(self):
        if not os.path.exists(self.__ROOT_DIR):
            os.makedirs(self.__ROOT_DIR)

    def __init__(self, file_name: str):
        self._create_root_dir()

        self.__file_name = file_name
        self.__data = ""
        
        
        self.__full_path = os.path.join(self.__ROOT_DIR, str(hashlib.md5(str.encode(self.__file_name)).hexdigest()))
        print("FULL PATH FOR: {} is : {}".format( file_name, self.__full_path))

        
        if not os.path.exists(self.__full_path):
            with open(self.__full_path, "a") as handle:
                handle.write("# Notes for: {}".format(os.path.basename(file_name)))

    def get_lines(self) -> list:
        with open(self.__full_path, "r") as handle:
            self.__data = handle.read()

        return self.__data.split("\n")

    def dump(self, lines: list[str]):
        lines = ['{}\n'.format(x) for x in lines if "Debug" not in x]

        # dirty
        if lines[-1] == "\n":
            lines = lines[:-2]

        print("LINESS TO WRITE", lines)

        with open(self.__full_path, "w") as handle:
            handle.writelines(lines)

    
    @classmethod
    def check_file_exists(cls, file_name: str) -> bool:
        full_path = os.path.join(cls.__ROOT_DIR, str(hashlib.md5(str.encode(file_name)).hexdigest()))
        return os.path.exists(full_path)
        
