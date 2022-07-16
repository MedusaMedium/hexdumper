BYTE_LEN = (2)
CHUNK_DEFAULT = 16
PADDING_CHAR = ' '
BYTE_DISPLAY_LEN = BYTE_LEN + len(PADDING_CHAR)


class PaddingMixin():
    def __init__(self, *args, 
                chunk:int=CHUNK_DEFAULT, 
                split_char:str="", 
                **kwargs):
        self.chunk = chunk
        self.split_char = split_char


    @property
    def split_char(self) -> str:
        return self._split_char
    @split_char.setter
    def split_char(self, char):
        self._split_char = char + PADDING_CHAR


    @property
    def byte_display_maxlen(self) -> int:
        return self.chunk * BYTE_DISPLAY_LEN


    @property
    def split_position(self) -> int:
        return (self.byte_display_maxlen // 2) + 2 * (self.chunk % 2)


    def pad_halfway_split(self, string:str) -> str:
        if len(string) > self.split_position:
            new_string =  string[:self.split_position]
            new_string += self.split_char
            new_string += string[self.split_position:]
            string = new_string
        return string


    def pad_end(self, string:str) -> str:
        pad_len = (self.byte_display_maxlen + len(self.split_char) - len(string))
        return string + PADDING_CHAR * pad_len