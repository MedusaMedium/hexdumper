from utils import formatting, utils


NON_ASCII_REPLACEMENT = "."


@utils.add_arithmetic_methods
class Dump(bytes, formatting.PaddingMixin):
    def __init__(self, *args, non_ascii:str=NON_ASCII_REPLACEMENT, **kwargs) -> None:
        self.non_ascii = non_ascii
        super().__init__(*args, **kwargs)


    def _hexdump(self, bytestring:bytes) -> str:
        ret_str = []
        buffer = b""
        done = False
        index = 0

        if self.chunk > len(bytestring):
            self.chunk = len(bytestring)

        while not done:
            if self.chunk < len(bytestring):
                buffer = bytestring[:self.chunk]
                bytestring = bytestring[self.chunk:]
            else:
                buffer = bytestring
                done = True

            # format each byte into a string
            hex_list = [f"{i:02x}" for i in buffer]
            # pack bytes together
            hex_str = formatting.PADDING_CHAR.join(hex_list) 
            # insert extra space between groups of 8 hex values
            hex_str = self.pad_halfway_split(hex_str)
            
            # pad the end of the hex string for consistency
            hex_str = self.pad_end(hex_str)

            # ascii string; chained comparison
            asc_str = "".join([chr(i) if 32 <= i <= 127 else self.non_ascii for i in buffer])

            # format hex and ascii strings 
            ret_str.append(f"{index * self.chunk:08x}  {hex_str} |{asc_str}|")

            index += 1
        
        return '\n'.join(ret_str)


    @property
    def dump(self) -> str:
        return self._hexdump(self)


    def __repr__(self) -> str:
        return super().__repr__()


    def __str__(self) -> str:
        return self.dump