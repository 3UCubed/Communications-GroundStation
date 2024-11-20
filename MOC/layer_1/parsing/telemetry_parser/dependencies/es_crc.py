class crc_util:
    def crc16(data: bytes, seed: int = 0xFFFF, poly: int = 0x1021):
        '''
        CRC-16-CCITT Algorithm
        '''
        data = bytearray(data)
        crc = seed
        for b in data:
            cur_byte = 0xFF & b
            crc ^= cur_byte << 0x8

            for _ in range(0, 8):
                if (crc & 0x8000):
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1

            crc = crc & 0xFFFF

        return crc & 0xFFFF
