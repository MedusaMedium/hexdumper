from mixins import padding


CHUNK_DEFAULT = 16
NON_ASCII_REPLACEMENT = "."


class Dump(padding.PaddingMixin):
    def __init__(self, 
                byte_string:bytes=b"", 
                chunk:int=CHUNK_DEFAULT, 
                non_ascii=NON_ASCII_REPLACEMENT, 
                *args, **kwargs):
        
        self.byte_string = byte_string
        self.chunk = chunk
        self.non_ascii = non_ascii
        super().__init__(*args, **kwargs)
        self._parse_byte_string()


    def _parse_byte_string(self):
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
        temp = self.byte_string
        buffer = b""
        done = False
        index = 0

        while not done:
            line = {}

            if self.chunk < len(temp):
                buffer = temp[:self.chunk]
                temp = temp[self.chunk:]
            else:
                buffer = temp
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


    def __repr__(self):
        return str(self.byte_string)


    def __str__(self)->str:
        return self._hexdump()


'''some other name ideas for this one:
DoubleDump, PumpDump, 
'''
class DumpEx(Dump):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @property
    def ascii_chunks(self): return None


    def search(self, needle_asc, needle_byt):pass