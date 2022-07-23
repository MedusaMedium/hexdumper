'''all the bells and whistles
- rich formatting
- byte and ascii searching
'''
from dump import Dump
from utils import formatting, utils

NON_ASCII_REPLACEMENT = "."


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
            hex_str = formatting.PADDING_CHAR.join(line['bytes_list']) 
            
            # insert extra space between groups of 8 hex values
            hex_str = self._pad_halfway_split(hex_str)
            
            # pad the end of the hex string for consistency
            hex_str = self._pad_end(hex_str)

            asc_str = [c if c else self.non_ascii for c in line['ascii_list']]
            asc_str = "".join(asc_str)

            # format hex and ascii strings 
            ret_arr.append(f"{line['linenum']}  {hex_str} |{asc_str}|")
        
        return '\n'.join(ret_arr)