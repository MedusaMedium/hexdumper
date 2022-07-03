BYTE_LEN = (2)
PADDING_CHAR = ' '
BYTE_DISPLAY_LEN = BYTE_LEN + len(PADDING_CHAR)


import os;file = os.path.basename(__file__)


# class PaddingMixin(object):
class Padding(object):
    # def __new__(obj, chunk:int=BYTE_LEN, split_char:str=""):
    #     obj.byte_display_maxlen = chunk * BYTE_DISPLAY_LEN
    #     obj.split_char = split_char + PADDING_CHAR
    #     obj.split_position = (obj.byte_display_maxlen // 2) + 2 * (chunk % 2)
    #     return super().__new__(obj)


    def __init__(self, chunk:int=BYTE_LEN, split_char:str=""):
        self.chunk = chunk
        self.split_char = split_char
        # self.byte_display_maxlen = self.chunk * BYTE_DISPLAY_LEN
        # self.split_char = split_char + PADDING_CHAR
        # self.split_position = (self.byte_display_maxlen // 2) + 2 * (self.chunk % 2)


    @property
    def chunk(self):
        return self._chunk
    @chunk.setter
    def chunk(self, c:int):
        print(f"{file}: pad.chunk.setter")
        self._chunk = c
        print(f"{file}: {self.chunk = }")
    

    @property
    def split_char(self):
        return self._split_char
    @split_char.setter
    def split_char(self, char):
        self._split_char = char + PADDING_CHAR
    
    
    @property
    def byte_display_maxlen(self):
        return self.chunk * BYTE_DISPLAY_LEN


    @property
    def split_position(self):
        return (self.byte_display_maxlen // 2) + 2 * (self.chunk % 2)
    


    def _pad_halfway_split(self, string:str)->str:
        if len(string) > self.split_position:
            new_string =  string[:self.split_position]
            new_string += self.split_char
            new_string += string[self.split_position:]
            string = new_string
        return string


    def _pad_end(self, string:str)->str:
        pad_len = (self.byte_display_maxlen + len(self.split_char) - len(string))
        return string + PADDING_CHAR * pad_len