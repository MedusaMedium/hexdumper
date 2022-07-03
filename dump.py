from collections import abc

from mixins import padding
from utils.inheritance import add_arithmetic_methods


CHUNK_DEFAULT = 16
NON_ASCII_REPLACEMENT = "."

BYTE_LEN = (2)
PADDING_CHAR = ' '
BYTE_DISPLAY_LEN = BYTE_LEN + len(PADDING_CHAR)


import os;file = os.path.basename(__file__)


# collections.abc.ByteString
# padding.PaddingMixin,
 
# @add_arithmetic_methods(target_methods=dir(bytes))
@add_arithmetic_methods
class Dump(bytes, object):
    def __new__(obj, source, 
                chunk:int=CHUNK_DEFAULT, 
                non_ascii:str=NON_ASCII_REPLACEMENT,
                split_char:str="",
                *args, **kwargs):
        obj.non_ascii = non_ascii
        obj.split_char = split_char
        # obj.pad = padding.Padding(chunk, obj.split_char)
        obj.chunk = chunk
        return super().__new__(obj, source=source, *args, **kwargs)


    # def __init__(self, source,
                # chunk:int=CHUNK_DEFAULT, 
                # non_ascii:str=NON_ASCII_REPLACEMENT,
                # split_char:str="",
        #         *args, **kwargs):
        # self.chunk = chunk
        # self.non_ascii = non_ascii
        # self.split_char = split_char
        # self.pad = padding.Padding(self.chunk, self.split_char)
                # non_ascii:str=NON_ASCII_REPLACEMENT, 
                # *args, **kwargs):
        # self.chunk = chunk
        # self.non_ascii = non_ascii
        # print(f"{self.non_ascii = }")
        # super().__init__(*args, **kwargs)
    

    @property
    def chunk(self):
        return self._chunk
    @chunk.setter
    def chunk(self, chunk):
        print(f"{file}: chunk.setter")
        self._chunk = chunk
        print(f"{file}: {self.chunk = }")
        # if hasattr(self, "pad"):
        #     print("setting pad attr")
        # self.pad.chunk = chunk
        # print(f"{file}: {self.pad.chunk = }")


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
    
    
    # @property
    # def split_char(self):
    #     return self.pad.split_char
    # @split_char.setter
    # def split_char(self, char):
    #     self.pad.split_char = char
        # self = self.refresh_padding
        # self.refresh_padding
        # self.pad = padding.Padding(self.chunk, self.split_char)



    def _hexdump(self, bytestring:bytes)->str:
        ret_str = []
        buffer = b""
        done = False
        index = 0

        while not done:
            if self.chunk < len(bytestring):
                buffer = bytestring[:self.chunk]
                bytestring = bytestring[self.chunk:]
            else:
                buffer = bytestring
                done = True

            # hex list
            hex_list = [f"{i:02x}" for i in buffer]
            # hex string
            hex_str = padding.PADDING_CHAR.join(hex_list) 
            # insert extra space between groups of 8 hex values
            hex_str = self._pad_halfway_split(hex_str)
            # hex_str = self.pad._pad_halfway_split(hex_str)
            # pad the end of the hex string for consistency
            hex_str = self._pad_end(hex_str)
            # hex_str = self.pad._pad_end(hex_str)

            # ascii string; chained comparison
            asc_str = "".join([chr(i) if 32 <= i <= 127 else self.non_ascii for i in buffer])

            # format hex and ascii strings 
            ret_str.append(f"{index * self.chunk:08x}  {hex_str}  |{asc_str}|")

            index += 1
        
        return '\n'.join(ret_str)


    def __repr__(self):
        return bytes.__repr__(self)


    def __str__(self)->str:
        return self._hexdump(self)


'''some other name ideas for this one:
DoubleDump, PumpDump, 
'''
# class DumpEx():
class DumpEx(Dump):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @property
    def ascii_chunks(self): return None


    def search(self, needle_asc, needle_byt, snippit):pass


    def _parse_bytes(self, new_byte_string:bytes):
        '''self.lines = [
            {
                'linenum':    '000008',
                'bytes':      b'\x01\x02\x03\x41\x42\x43',
                'bytes_list': ['01', '02', '03', '41', '42', '43']
                'ascii_list': [None, None, None,  'A',  'B',  'C']
            },
            ...
        ]
        '''
        lines = []
        buffer = b""
        done = False
        index = 0

        while not done:
            line = {}

            if self.chunk < len(new_byte_string):
                buffer = new_byte_string[:self.chunk]
                new_byte_string = new_byte_string[self.chunk:]
            else:
                buffer = new_byte_string
                done = True

            line['linenum'] = f"{index * self.chunk:08x}"
            line['bytes'] = buffer
            line['bytes_list'] = [f"{i:02x}" for i in buffer]
            line['ascii_list'] = [chr(i) if 32 <= i <= 127 else None for i in buffer]
            
            lines.append(line)
            index += 1
        self.lines = lines


    def _hexdump(self)->str:
        ret_arr = []
        for line in self.lines:
           # hex string
            hex_str = padding.PADDING_CHAR.join(line['bytes_list']) 
            
            # insert extra space between groups of 8 hex values
            hex_str = self._pad_halfway_split(hex_str)
            
            # pad the end of the hex string for consistency
            hex_str = self._pad_end(hex_str)

            asc_str = [c if c else self.non_ascii for c in line['ascii_list']]
            asc_str = "".join(asc_str)

            # format hex and ascii strings 
            ret_arr.append(f"{line['linenum']}  {hex_str} |{asc_str}|")
        
        return '\n'.join(ret_arr)