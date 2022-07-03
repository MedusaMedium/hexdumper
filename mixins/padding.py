BYTE_LEN = (2)
PADDING_CHAR = ' '
BYTE_DISPLAY_LEN = BYTE_LEN + len(PADDING_CHAR)


import os;file = os.path.basename(__file__)


class PaddingMixin(object):
    def __init__(self, split_char:str=""):
        try:
            chunk = self.chunk
            print(f"{file}: self.chunk exists")
        except AttributeError: 
            print(f"{file}: self.chunk DNE")
            chunk = BYTE_LEN
        
        # print(f"{file}: {type(chunk) = }\n{file}: {chunk = }")
        self.byte_display_maxlen = chunk * BYTE_DISPLAY_LEN
        # print(f"{file}: {type(self.byte_display_maxlen) = }\n{file}: {self.byte_display_maxlen = }")
        self.split_char = split_char + PADDING_CHAR
        self.split_position = (self.byte_display_maxlen // 2) + 2 * (chunk % 2)


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