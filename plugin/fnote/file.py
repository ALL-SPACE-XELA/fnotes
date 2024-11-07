import os
import hashlib
from datetime import datetime
from enum import Enum
import re

from typing import Optional

NEW_LINE_RULE = re.compile(r'(\n)\1{3,}')


class TimestampType(Enum):
    Created = 1
    Edited = 2

def add_timestamp(timestamp_type: TimestampType):
    date_today = datetime.now().strftime("%d/%m/%Y")
    match timestamp_type:
        case TimestampType.Created:
            return """<!---Created: {} -->\n""".format(date_today)
        case TimestampType.Edited:
            return """<!---Edited: {} -->""".format(date_today)

class NFile:

    # .local/share/nvim
    __ROOT_DIR = os.path.expanduser("~/.local/share/nvim/fnote-vim")

    def get_root_dir(self):
        return self.__ROOT_DIR

    def _create_root_dir(self):
        if not os.path.exists(self.__ROOT_DIR):
            os.makedirs(self.__ROOT_DIR)

    def __init__(self, file_name: str, root_dir: Optional[str] = None):
        if root_dir:
            # mainly for testing purposes...
            self.__ROOT_DIR = root_dir

        self._create_root_dir()

        self.__file_name = file_name
        self.__data = ""
        
        
        self.__full_path = os.path.join(self.__ROOT_DIR, str(hashlib.md5(str.encode(self.__file_name)).hexdigest()))
        print("FULL PATH FOR: {} is : {}".format( file_name, self.__full_path))

        
        if not os.path.exists(self.__full_path):
            with open(self.__full_path, "a") as handle:
                handle.write("# Notes for: {}\n\n".format(os.path.basename(file_name)))
                handle.write(add_timestamp(TimestampType.Created))
                handle.write(add_timestamp(TimestampType.Edited))

    def get_lines(self) -> list:
        with open(self.__full_path, "r") as handle:
            self.__data = handle.read()

        lines = self.__data.split("\n")
        if len(lines) > 5:
            # 5 because I'm assuming a title, created and edited timestamp
            # and a couple lines of notes
            lines.append(add_timestamp(TimestampType.Edited))
        return lines

    def process(self, lines: list[str]) -> str:
        lines = ['{}\n'.format(x) for x in lines if "Debug" not in x]

        # as a rule, I will not allow more than 2 consecutive new lines
        lines = ''.join(lines)
        lines = re.sub(NEW_LINE_RULE, '\n\n', lines).strip()
        lines = lines.split("\n")

        # if we did not make any changes (last line is the "edited line"), we revert it
        if add_timestamp(TimestampType.Edited) in lines[-2]:
            lines = lines[:-2]
        lines = "\n".join(lines)
        return lines


    def dump(self, lines: str):
        lines = self.process(lines)
        with open(self.__full_path, "w") as handle:
            handle.write(lines)

    
    @classmethod
    def check_file_exists(cls, file_name: str) -> bool:
        full_path = os.path.join(cls.__ROOT_DIR, str(hashlib.md5(str.encode(file_name)).hexdigest()))
        return os.path.exists(full_path)
        
