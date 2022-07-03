from mixins import padding


CHUNK_DEFAULT = 16
NON_ASCII_REPLACEMENT = "."

# collections.abc.ByteString
# padding.PaddingMixin, 
class Dump(bytes, padding.PaddingMixin):
    def __new__(obj, source, 
                chunk:int=CHUNK_DEFAULT, 
                non_ascii:str=NON_ASCII_REPLACEMENT, 
                *args, **kwargs):
        # source:bytes=b"", 
        obj.chunk = chunk
        obj.source = source
        obj.non_ascii = non_ascii
        # obj = padding.PaddingMixin.__new__(obj, *args, **kwargs)
        # return bytearray.__new__(obj, source, *args, **kwargs)
        return super().__new__(obj, source, *args, **kwargs)


    def __init__(self, 
                non_ascii:str=NON_ASCII_REPLACEMENT, 
                # chunk:int=CHUNK_DEFAULT, 
                *args, **kwargs):
        # print(f"DUMP: {source = }")
        # self.chunk = chunk
        # self.non_ascii = non_ascii
        print(f"{self.non_ascii = }")
        # print(f"{super().__init__ = }")
        # kwargs['source'] = source
        super().__init__(*args, **kwargs)
        # self.source = source


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
            # pad the end of the hex string for consistency
            hex_str = self._pad_end(hex_str)

            # ascii string; chained comparison
            asc_str = "".join([chr(i) if 32 <= i <= 127 else self.non_ascii for i in buffer])

            # format hex and ascii strings 
            ret_str.append(f"{index * self.chunk:08x}  {hex_str}  |{asc_str}|")

            index += 1
        
        return '\n'.join(ret_str)
    

    def __add__(self, additive):
        print(f"{additive = }")
        print(f"{additive + self = }")
        src = self + additive
        return self.__new__(self, source = src)


    def __repr__(self):
        return bytes.__repr__(self)


    def __str__(self)->str:
        return self._hexdump(self)


'''some other name ideas for this one:
DoubleDump, PumpDump, 
'''
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