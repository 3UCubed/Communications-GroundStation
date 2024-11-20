# ********************************************************************************************
# * @file SerDesHelpers.py
# * @brief Python SerDes Helpers implementation generator
# ********************************************************************************************
# * @version           
# *
# * @copyright         (C) Copyright EnduroSat
# *
# *                    Contents and presentations are protected world-wide.
# *                    Any kind of using, copying etc. is prohibited without prior permission.
# *                    All rights - incl. industrial property rights - are reserved.
# *
# *-------------------------------------------------------------------------------------------
# * GENERATOR: org.endurosat.generators.macchiato.binders.Gen_Py v1.11
# *-------------------------------------------------------------------------------------------
# * !!! Please note that this code is fully GENERATED and shall not be manually modified as
# * all changes will be overwritten !!!
# ********************************************************************************************

from struct import pack, unpack


class SerDesHelpers:
    basicTypesDict = {}

    basicTypesDict['uint8'] = (1, False)
    basicTypesDict['uint16'] = (2, False)
    basicTypesDict['uint32'] = (4, False)
    basicTypesDict['uint64'] = (8, False)
    basicTypesDict['int8'] = (1, True)
    basicTypesDict['int16'] = (2, True)
    basicTypesDict['int32'] = (4, True)
    basicTypesDict['int64'] = (8, True)
    basicTypesDict['boolean'] = (1, False)

    class serdesType_Helpers:
        @staticmethod
        def extractBytes(data, pos, byteCount):
            byteStrip = []
            for i in range(pos, pos + byteCount):
                byteStrip.append(data[i])

            return bytes(byteStrip)

    class serdesType_Base:
        byteOrder = 'little'

        @staticmethod
        def getPackByteOrderPrefix():
            if SerDesHelpers.serdesType_Base.byteOrder == 'little':
                return '<'
            else:
                return '>'

    class serdesType_basic:
        @staticmethod
        def serialize(basicTypeName, val):
            if basicTypeName in SerDesHelpers.basicTypesDict:
                return val.to_bytes(SerDesHelpers.basicTypesDict[basicTypeName][0],
                                    byteorder=SerDesHelpers.serdesType_Base.byteOrder,
                                    signed=SerDesHelpers.basicTypesDict[basicTypeName][1])
            else:
                raise TypeError('Unknown basic type: "' +
                                SerDesHelpers.basicTypesDict + '"')

        @staticmethod
        # returns a tuple: (deserialized value, number of bytes processed)
        def deserialize(basicTypeName, data, pos):
            if basicTypeName in SerDesHelpers.basicTypesDict:
                return (int.from_bytes(SerDesHelpers.serdesType_Helpers.extractBytes(data, pos, SerDesHelpers.basicTypesDict[basicTypeName][0]),
                                       byteorder=SerDesHelpers.serdesType_Base.byteOrder,
                                       signed=SerDesHelpers.basicTypesDict[basicTypeName][1]),
                        SerDesHelpers.basicTypesDict[basicTypeName][0])
            else:
                raise TypeError('Unknown basic type: "' +
                                SerDesHelpers.basicTypesDict + '"')

    class serdesType_float:
        @staticmethod
        def serialize(val):
            return pack(SerDesHelpers.serdesType_Base.getPackByteOrderPrefix() + "f", val)

        @staticmethod
        # returns a tuple: (deserialized value, number of bytes processed)
        def deserialize(data, pos):
            return (unpack(SerDesHelpers.serdesType_Base.getPackByteOrderPrefix() + "f",
                    SerDesHelpers.serdesType_Helpers.extractBytes(data, pos, SerDesHelpers.serdesType_float.getSize()))[0],
                    SerDesHelpers.serdesType_float.getSize())

        @staticmethod
        def getSize():
            return 4

    class serdesType_double:
        @staticmethod
        def serialize(val):
            return pack(SerDesHelpers.serdesType_Base.getPackByteOrderPrefix() + "d", val)

        @staticmethod
        # returns a tuple: (deserialized value, number of bytes processed)
        def deserialize(data, pos):
            return (unpack(SerDesHelpers.serdesType_Base.getPackByteOrderPrefix() + "d",
                    SerDesHelpers.serdesType_Helpers.extractBytes(data, pos, SerDesHelpers.serdesType_double.getSize()))[0],
                    SerDesHelpers.serdesType_double.getSize())

        @staticmethod
        def getSize():
            return 8

    class serdesType_basicArray:
        @staticmethod
        def serialize(basicTypeName, array, total_array_size):
            result = bytearray()

            for i in array:
                result += SerDesHelpers.serdesType_basic.serialize(
                    basicTypeName, i)

            # Complete the array size
            total_bytes_size = total_array_size * SerDesHelpers.basicTypesDict[basicTypeName][0]
            for _ in range(len(result), total_bytes_size):
                result.append(0)

            return result

        @staticmethod
        def deserialize(basicTypeName, data, pos, size):
            result = []

            rawDataStrip = SerDesHelpers.serdesType_Helpers.extractBytes(data,
                                                                         pos,
                                                                         size * SerDesHelpers.basicTypesDict[basicTypeName][0])

            currentPos = 0

            for _ in range(0, size):
                (val, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize(
                    basicTypeName, rawDataStrip, currentPos)
                result.append(val)
                currentPos += bytesProcessed

            return (result, size * SerDesHelpers.basicTypesDict[basicTypeName][0])

    class serdesType_floatDoubleArray:
        @staticmethod
        def serialize(serdesType, array, total_array_size):
            result = bytearray()

            for i in array:
                result += serdesType.serialize(i)

            # Complete the array size
            total_bytes_size = total_array_size * serdesType.getSize()
            for _ in range(len(result), total_bytes_size):
                result.append(0)

            return result

        @staticmethod
        def deserialize(serdesType, data, pos, size):
            result = []

            rawDataStrip = SerDesHelpers.serdesType_Helpers.extractBytes(data,
                                                                         pos,
                                                                         size * serdesType.getSize())

            currentPos = 0

            if 'float' in str(serdesType):
                type_instance = SerDesHelpers.serdesType_float
            elif 'double' in str(serdesType):
                type_instance = SerDesHelpers.serdesType_double
            else:
                raise TypeError(
                    f'serdesType shall be a reference to either serdesType_float or serdesType_double class: "{str(serdesType)}" provided instead')

            for _ in range(0, size):
                (val, bytesProcessed) = type_instance.deserialize(
                    rawDataStrip, currentPos)
                result.append(val)
                currentPos += bytesProcessed

            return (result, size * serdesType.getSize())

    class serdesType_customTypeArray:
        @staticmethod
        def serialize(array, total_array_size):
            result = bytearray()

            for entry in array:
                result += entry.serialize()

            # Complete the array size
            total_bytes_size = total_array_size * array[0].getSize()
            for _ in range(len(result), total_bytes_size):
                result.append(0)

            return result

        @staticmethod
        def deserialize(customTypeSerDesType, data, pos, size):
            result = []

            rawDataStrip = SerDesHelpers.serdesType_Helpers.extractBytes(data,
                                                                         pos,
                                                                         size * customTypeSerDesType.getSize())

            currentPos = 0

            for _ in range(0, size):
                (val, bytesProcessed) = customTypeSerDesType.deserialize(
                    rawDataStrip, currentPos)
                result.append(val)
                currentPos += bytesProcessed

            return (result, size * customTypeSerDesType.getSize())

    class struct_FPHeader:
        def __init__(self):
            self.u16ProtoId = 0
            self.u32FuncId = 0
            self.u16seqId = 0
            self.u8ErrCode = 0

        def serialize(self):
            result = bytearray()

            result += SerDesHelpers.serdesType_basic.serialize(
                'uint16', self.u16ProtoId)
            result += SerDesHelpers.serdesType_basic.serialize(
                'uint32', self.u32FuncId)
            result += SerDesHelpers.serdesType_basic.serialize(
                'uint16', self.u16seqId)
            result += SerDesHelpers.serdesType_basic.serialize(
                'uint8', self.u8ErrCode)

            return result

        @staticmethod
        def deserialize(data, pos):
            resultInstance = SerDesHelpers.struct_FPHeader()

            currentPos = 0
            (resultInstance.u16ProtoId, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize(
                'uint16', data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.u32FuncId, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize(
                'uint32', data, currentPos)
            # strip-down response bit
            resultInstance.u32FuncId &= ~(0x80000000)
            currentPos += bytesProcessed
            (resultInstance.u16seqId, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize(
                'uint16', data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.u8ErrCode, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize(
                'uint8', data, currentPos)
            currentPos += bytesProcessed

            return (resultInstance, currentPos)

        @staticmethod
        def getSize():
            return 9

    class serdesType_string:

        @staticmethod
        def serialize(asciiString, total_string_size):
            assert total_string_size >= len(asciiString)
            asciiString += ('\0' * (total_string_size - len(asciiString)))
            return asciiString.encode('ascii')

        @staticmethod
        def deserialize(data, pos, size):
            rawDataStrip = SerDesHelpers.serdesType_Helpers.extractBytes(data,
                                                                         pos,
                                                                         size)
            return (rawDataStrip.decode('ascii'), size)
