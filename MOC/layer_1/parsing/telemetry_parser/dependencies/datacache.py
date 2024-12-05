# ********************************************************************************************
# * @file datacache.py
# * @brief Data Cache Deserializer Routines generation
# ********************************************************************************************
# * @version           interface data_cache v0.1
# *
# * @copyright         (C) Copyright EnduroSat
# *
# *                    Contents and presentations are protected world-wide.
# *                    Any kind of using, copying etc. is prohibited without prior permission.
# *                    All rights - incl. industrial property rights - are reserved.
# *
# *-------------------------------------------------------------------------------------------
# * GENERATOR: org.endurosat.generators.macchiato.binders.Gen_DC v0.7
# *-------------------------------------------------------------------------------------------
# * !!! Please note that this code is fully GENERATED and shall not be manually modified as
# * all changes will be overwritten !!!
# ********************************************************************************************

from layer_1.parsing.telemetry_parser.SerDesHelpers import *

class dc_parser:
    NUM_TASKS = 0
    def __init__(self, num_tasks):
        dc_parser.NUM_TASKS = num_tasks
        self.dc_entries_dict = {}

        self.dc_entries_dict[0x00000010] = dc_parser.struct_OBC_0
        self.dc_entries_dict[0x00000011] = dc_parser.struct_ADCS_0
        self.dc_entries_dict[0x00000012] = dc_parser.struct_ADCS_1
        self.dc_entries_dict[0x00000013] = dc_parser.struct_ADCS_2
        self.dc_entries_dict[0x00000014] = dc_parser.struct_EPS_0
        self.dc_entries_dict[0x00000015] = dc_parser.struct_SSP_0
        self.dc_entries_dict[0x00000016] = dc_parser.struct_SSP_1
        self.dc_entries_dict[0x00000017] = dc_parser.struct_SSP_2
        self.dc_entries_dict[0x00000019] = dc_parser.struct_AOCS_CNTRL_TLM
        self.dc_entries_dict[0x0000001A] = dc_parser.struct_EPS_1
        self.dc_entries_dict[0x0000001B] = dc_parser.struct_EPS_2
        self.dc_entries_dict[0x0000001C] = dc_parser.struct_EPS_3
        self.dc_entries_dict[0x0000001D] = dc_parser.struct_EPS_4
        self.dc_entries_dict[0x0000001E] = dc_parser.struct_EPS_5
        self.dc_entries_dict[0x0000001F] = dc_parser.struct_EPS_6
        self.dc_entries_dict[0x00000020] = dc_parser.struct_TaskStats
        self.dc_entries_dict[0x00000021] = dc_parser.struct_SSP_3
        self.dc_entries_dict[0x00000022] = dc_parser.struct_SENSOR_MAG_PRIMARY
        self.dc_entries_dict[0x00000023] = dc_parser.struct_SENSOR_MAG_SECONDARY
        self.dc_entries_dict[0x00000024] = dc_parser.struct_SENSOR_GYRO
        self.dc_entries_dict[0x00000025] = dc_parser.struct_SENSOR_COARSE_SUN
        self.dc_entries_dict[0x00000026] = dc_parser.struct_ES_ADCS_SENSOR_MAG_PRIMARY
        self.dc_entries_dict[0x00000027] = dc_parser.struct_ES_ADCS_SENSOR_MAG_SECONDARY
        self.dc_entries_dict[0x00000028] = dc_parser.struct_ES_ADCS_SENSOR_GYRO
        self.dc_entries_dict[0x00000029] = dc_parser.struct_ES_ADCS_SENSOR_CSS
        self.dc_entries_dict[0x00000030] = dc_parser.struct_ES_ADCS_ESTIMATES_BDOT
        self.dc_entries_dict[0x00000031] = dc_parser.struct_ES_ADCS_CONTROL_VALUES_MTQ
        self.dc_entries_dict[0x00000032] = dc_parser.struct_ConOpsFlags
        self.dc_entries_dict[0x00000033] = dc_parser.struct_AOCS_CNTRL_SYS_STATE
        self.dc_entries_dict[0x00000034] = dc_parser.struct_ADCS_3
        self.dc_entries_dict[0x00000035] = dc_parser.struct_ADCS_4

    def parse_by_id(self, id : int, data : bytes) -> any:
        if id in self.dc_entries_dict:
            return self.dc_entries_dict[id].deserialize(data, 0)
        else:
            return None
    
    class struct_OBC_0:
        def __init__(self, uint8__opMode = 0, uint32__upTime = 0, uint16__totalResetCount = 0, uint16__resetReasonBitField = 0, uint16__payloadModesStatus = 0):
            self.uint8__opMode = uint8__opMode
            self.uint32__upTime = uint32__upTime
            self.uint16__totalResetCount = uint16__totalResetCount
            self.uint16__resetReasonBitField = uint16__resetReasonBitField
            self.uint16__payloadModesStatus = uint16__payloadModesStatus
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__opMode)
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__upTime)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__totalResetCount)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__resetReasonBitField)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__payloadModesStatus)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_OBC_0()
    
            currentPos = pos
            (resultInstance.uint8__opMode, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint32__upTime, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__totalResetCount, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__resetReasonBitField, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__payloadModesStatus, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 11
    
    class struct_ADCS_0:
        def __init__(self, a__int16__magFieldVec = [], a__int16__coarseSunVec = [], a__int16__fineSunVec = [], a__int16__nadirVec = [], a__int16__angRateVec = [], a__int16__wheelSpeedArr = []):
            self.a__int16__magFieldVec = a__int16__magFieldVec
            self.a__int16__coarseSunVec = a__int16__coarseSunVec
            self.a__int16__fineSunVec = a__int16__fineSunVec
            self.a__int16__nadirVec = a__int16__nadirVec
            self.a__int16__angRateVec = a__int16__angRateVec
            self.a__int16__wheelSpeedArr = a__int16__wheelSpeedArr
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__magFieldVec)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__coarseSunVec)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__fineSunVec)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__nadirVec)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__angRateVec)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__wheelSpeedArr)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ADCS_0()
    
            currentPos = pos
            (resultInstance.a__int16__magFieldVec, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 3)
            currentPos += bytesProcessed
            (resultInstance.a__int16__coarseSunVec, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 3)
            currentPos += bytesProcessed
            (resultInstance.a__int16__fineSunVec, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 3)
            currentPos += bytesProcessed
            (resultInstance.a__int16__nadirVec, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 3)
            currentPos += bytesProcessed
            (resultInstance.a__int16__angRateVec, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 3)
            currentPos += bytesProcessed
            (resultInstance.a__int16__wheelSpeedArr, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 3)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 36
    
    class struct_ADCS_1:
        def __init__(self, a__int16__estQSet = [], a__int16__estAngRateVec = []):
            self.a__int16__estQSet = a__int16__estQSet
            self.a__int16__estAngRateVec = a__int16__estAngRateVec
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__estQSet)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__estAngRateVec)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ADCS_1()
    
            currentPos = pos
            (resultInstance.a__int16__estQSet, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 3)
            currentPos += bytesProcessed
            (resultInstance.a__int16__estAngRateVec, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 3)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_ADCS_2:
        def __init__(self, a__uint8__adcsState = []):
            self.a__uint8__adcsState = a__uint8__adcsState
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basicArray.serialize("uint8", self.a__uint8__adcsState)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ADCS_2()
    
            currentPos = pos
            (resultInstance.a__uint8__adcsState, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("uint8", data, currentPos, 6)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 6
    
    class struct_EPS_0:
        def __init__(self, int64__battEnergy = 0, int64__battCharge = 0, int64__battChargeCapacity = 0, int64__battPercent = 0, int32__battVoltage = 0, int32__battCurrent = 0, int32__battTemperature = 0):
            self.int64__battEnergy = int64__battEnergy
            self.int64__battCharge = int64__battCharge
            self.int64__battChargeCapacity = int64__battChargeCapacity
            self.int64__battPercent = int64__battPercent
            self.int32__battVoltage = int32__battVoltage
            self.int32__battCurrent = int32__battCurrent
            self.int32__battTemperature = int32__battTemperature
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int64", self.int64__battEnergy)
            result += SerDesHelpers.serdesType_basic.serialize("int64", self.int64__battCharge)
            result += SerDesHelpers.serdesType_basic.serialize("int64", self.int64__battChargeCapacity)
            result += SerDesHelpers.serdesType_basic.serialize("int64", self.int64__battPercent)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__battVoltage)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__battCurrent)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__battTemperature)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_EPS_0()
    
            currentPos = pos
            (resultInstance.int64__battEnergy, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int64", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int64__battCharge, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int64", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int64__battChargeCapacity, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int64", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int64__battPercent, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int64", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__battVoltage, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__battCurrent, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__battTemperature, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 44
    
    class struct_SSP_0:
        def __init__(self, uint16__sunDataMain = 0, uint16__sunDataExt = 0, int16__tempMCU = 0, int16__tempMain = 0, int16__tempExt1 = 0, int16__tempExt2 = 0):
            self.uint16__sunDataMain = uint16__sunDataMain
            self.uint16__sunDataExt = uint16__sunDataExt
            self.int16__tempMCU = int16__tempMCU
            self.int16__tempMain = int16__tempMain
            self.int16__tempExt1 = int16__tempExt1
            self.int16__tempExt2 = int16__tempExt2
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__sunDataMain)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__sunDataExt)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempMCU)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempMain)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempExt1)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempExt2)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_SSP_0()
    
            currentPos = pos
            (resultInstance.uint16__sunDataMain, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__sunDataExt, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempMCU, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempMain, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempExt1, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempExt2, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_SSP_1:
        def __init__(self, uint16__sunDataMain = 0, uint16__sunDataExt = 0, int16__tempMCU = 0, int16__tempMain = 0, int16__tempExt1 = 0, int16__tempExt2 = 0):
            self.uint16__sunDataMain = uint16__sunDataMain
            self.uint16__sunDataExt = uint16__sunDataExt
            self.int16__tempMCU = int16__tempMCU
            self.int16__tempMain = int16__tempMain
            self.int16__tempExt1 = int16__tempExt1
            self.int16__tempExt2 = int16__tempExt2
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__sunDataMain)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__sunDataExt)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempMCU)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempMain)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempExt1)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempExt2)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_SSP_1()
    
            currentPos = pos
            (resultInstance.uint16__sunDataMain, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__sunDataExt, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempMCU, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempMain, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempExt1, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempExt2, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_SSP_2:
        def __init__(self, uint16__sunDataMain = 0, uint16__sunDataExt = 0, int16__tempMCU = 0, int16__tempMain = 0, int16__tempExt1 = 0, int16__tempExt2 = 0):
            self.uint16__sunDataMain = uint16__sunDataMain
            self.uint16__sunDataExt = uint16__sunDataExt
            self.int16__tempMCU = int16__tempMCU
            self.int16__tempMain = int16__tempMain
            self.int16__tempExt1 = int16__tempExt1
            self.int16__tempExt2 = int16__tempExt2
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__sunDataMain)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__sunDataExt)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempMCU)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempMain)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempExt1)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempExt2)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_SSP_2()
    
            currentPos = pos
            (resultInstance.uint16__sunDataMain, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__sunDataExt, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempMCU, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempMain, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempExt1, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempExt2, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_AOCS_CNTRL_TLM:
        def __init__(self, uint16__adcsErrFlags = 0, int32__estAngRateNorm = 0, a__int32__estAngRateVec = [], a__int32__estAttAngles = [], a__int16__measWheelSpeed = []):
            self.uint16__adcsErrFlags = uint16__adcsErrFlags
            self.int32__estAngRateNorm = int32__estAngRateNorm
            self.a__int32__estAngRateVec = a__int32__estAngRateVec
            self.a__int32__estAttAngles = a__int32__estAttAngles
            self.a__int16__measWheelSpeed = a__int16__measWheelSpeed
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__adcsErrFlags)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__estAngRateNorm)
            result += SerDesHelpers.serdesType_basicArray.serialize("int32", self.a__int32__estAngRateVec)
            result += SerDesHelpers.serdesType_basicArray.serialize("int32", self.a__int32__estAttAngles)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__measWheelSpeed)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_AOCS_CNTRL_TLM()
    
            currentPos = pos
            (resultInstance.uint16__adcsErrFlags, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__estAngRateNorm, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.a__int32__estAngRateVec, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int32", data, currentPos, 3)
            currentPos += bytesProcessed
            (resultInstance.a__int32__estAttAngles, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int32", data, currentPos, 3)
            currentPos += bytesProcessed
            (resultInstance.a__int16__measWheelSpeed, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 3)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 36
    
    class struct_EPS_1:
        def __init__(self, int32__battCapacity = 0, int32__battVoltage = 0, int32__battCurrent = 0, int32__battTemperature = 0):
            self.int32__battCapacity = int32__battCapacity
            self.int32__battVoltage = int32__battVoltage
            self.int32__battCurrent = int32__battCurrent
            self.int32__battTemperature = int32__battTemperature
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__battCapacity)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__battVoltage)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__battCurrent)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__battTemperature)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_EPS_1()
    
            currentPos = pos
            (resultInstance.int32__battCapacity, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__battVoltage, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__battCurrent, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__battTemperature, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 16
    
    class struct_EPS_2:
        def __init__(self, int16__VOLT_BRDSUP = 0, int16__TEMP_MCU = 0, int16__VIP_INPUT_Voltage = 0, int16__VIP_INPUT_Current = 0, int16__VIP_INPUT_Power = 0, uint16__STAT_CH_ON = 0, uint16__STAT_CH_OCF = 0, int16__VIP_Voltage_VD0 = 0, int16__VIP_Current_VD0 = 0, int16__VIP_Voltage_VD4 = 0, int16__VIP_Current_VD4 = 0, int16__VIP_Voltage_VD6 = 0, int16__VIP_Current_VD6 = 0, int16__VIP_Voltage_VD7 = 0, int16__VIP_Current_VD7 = 0, int16__VIP_Voltage_VD8 = 0, int16__VIP_Current_VD8 = 0, int16__VIP_Voltage_VD9 = 0, int16__VIP_Current_VD9 = 0, int16__VIP_Voltage_VD10 = 0, int16__VIP_Current_VD10 = 0, int16__VIP_Voltage_VD11 = 0, int16__VIP_Current_VD11 = 0):
            self.int16__VOLT_BRDSUP = int16__VOLT_BRDSUP
            self.int16__TEMP_MCU = int16__TEMP_MCU
            self.int16__VIP_INPUT_Voltage = int16__VIP_INPUT_Voltage
            self.int16__VIP_INPUT_Current = int16__VIP_INPUT_Current
            self.int16__VIP_INPUT_Power = int16__VIP_INPUT_Power
            self.uint16__STAT_CH_ON = uint16__STAT_CH_ON
            self.uint16__STAT_CH_OCF = uint16__STAT_CH_OCF
            self.int16__VIP_Voltage_VD0 = int16__VIP_Voltage_VD0
            self.int16__VIP_Current_VD0 = int16__VIP_Current_VD0
            self.int16__VIP_Voltage_VD4 = int16__VIP_Voltage_VD4
            self.int16__VIP_Current_VD4 = int16__VIP_Current_VD4
            self.int16__VIP_Voltage_VD6 = int16__VIP_Voltage_VD6
            self.int16__VIP_Current_VD6 = int16__VIP_Current_VD6
            self.int16__VIP_Voltage_VD7 = int16__VIP_Voltage_VD7
            self.int16__VIP_Current_VD7 = int16__VIP_Current_VD7
            self.int16__VIP_Voltage_VD8 = int16__VIP_Voltage_VD8
            self.int16__VIP_Current_VD8 = int16__VIP_Current_VD8
            self.int16__VIP_Voltage_VD9 = int16__VIP_Voltage_VD9
            self.int16__VIP_Current_VD9 = int16__VIP_Current_VD9
            self.int16__VIP_Voltage_VD10 = int16__VIP_Voltage_VD10
            self.int16__VIP_Current_VD10 = int16__VIP_Current_VD10
            self.int16__VIP_Voltage_VD11 = int16__VIP_Voltage_VD11
            self.int16__VIP_Current_VD11 = int16__VIP_Current_VD11
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VOLT_BRDSUP)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__TEMP_MCU)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_INPUT_Voltage)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_INPUT_Current)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_INPUT_Power)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__STAT_CH_ON)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__STAT_CH_OCF)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Voltage_VD0)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Current_VD0)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Voltage_VD4)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Current_VD4)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Voltage_VD6)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Current_VD6)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Voltage_VD7)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Current_VD7)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Voltage_VD8)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Current_VD8)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Voltage_VD9)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Current_VD9)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Voltage_VD10)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Current_VD10)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Voltage_VD11)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_Current_VD11)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_EPS_2()
    
            currentPos = pos
            (resultInstance.int16__VOLT_BRDSUP, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__TEMP_MCU, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_INPUT_Voltage, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_INPUT_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_INPUT_Power, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__STAT_CH_ON, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__STAT_CH_OCF, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Voltage_VD0, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Current_VD0, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Voltage_VD4, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Current_VD4, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Voltage_VD6, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Current_VD6, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Voltage_VD7, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Current_VD7, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Voltage_VD8, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Current_VD8, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Voltage_VD9, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Current_VD9, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Voltage_VD10, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Current_VD10, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Voltage_VD11, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_Current_VD11, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 46
    
    class struct_EPS_3:
        def __init__(self, int16__VOLT_BRDSUP = 0, int16__TEMP_MCU = 0, int16__VIP_INPUT_Voltage = 0, int16__VIP_INPUT_Current = 0, int16__VIP_INPUT_Power = 0, uint16__STAT_BU = 0, a__int16__VIP_BP_INPUT_Voltage = [], a__int16__VIP_BP_INPUT_Current = [], a__int16__VIP_BP_INPUT_Power = [], a__int16__STAT_BP = [], a__int16__VOLT_CELL1 = [], a__int16__VOLT_CELL2 = [], a__int16__VOLT_CELL3 = [], a__int16__VOLT_CELL4 = [], a__int16__BAT_TEMP1 = [], a__int16__BAT_TEMP2 = [], a__int16__BAT_TEMP3 = []):
            self.int16__VOLT_BRDSUP = int16__VOLT_BRDSUP
            self.int16__TEMP_MCU = int16__TEMP_MCU
            self.int16__VIP_INPUT_Voltage = int16__VIP_INPUT_Voltage
            self.int16__VIP_INPUT_Current = int16__VIP_INPUT_Current
            self.int16__VIP_INPUT_Power = int16__VIP_INPUT_Power
            self.uint16__STAT_BU = uint16__STAT_BU
            self.a__int16__VIP_BP_INPUT_Voltage = a__int16__VIP_BP_INPUT_Voltage
            self.a__int16__VIP_BP_INPUT_Current = a__int16__VIP_BP_INPUT_Current
            self.a__int16__VIP_BP_INPUT_Power = a__int16__VIP_BP_INPUT_Power
            self.a__int16__STAT_BP = a__int16__STAT_BP
            self.a__int16__VOLT_CELL1 = a__int16__VOLT_CELL1
            self.a__int16__VOLT_CELL2 = a__int16__VOLT_CELL2
            self.a__int16__VOLT_CELL3 = a__int16__VOLT_CELL3
            self.a__int16__VOLT_CELL4 = a__int16__VOLT_CELL4
            self.a__int16__BAT_TEMP1 = a__int16__BAT_TEMP1
            self.a__int16__BAT_TEMP2 = a__int16__BAT_TEMP2
            self.a__int16__BAT_TEMP3 = a__int16__BAT_TEMP3
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VOLT_BRDSUP)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__TEMP_MCU)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_INPUT_Voltage)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_INPUT_Current)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_INPUT_Power)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__STAT_BU)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VIP_BP_INPUT_Voltage)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VIP_BP_INPUT_Current)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VIP_BP_INPUT_Power)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__STAT_BP)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VOLT_CELL1)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VOLT_CELL2)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VOLT_CELL3)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VOLT_CELL4)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__BAT_TEMP1)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__BAT_TEMP2)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__BAT_TEMP3)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_EPS_3()
    
            currentPos = pos
            (resultInstance.int16__VOLT_BRDSUP, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__TEMP_MCU, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_INPUT_Voltage, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_INPUT_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_INPUT_Power, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__STAT_BU, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VIP_BP_INPUT_Voltage, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VIP_BP_INPUT_Current, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VIP_BP_INPUT_Power, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__STAT_BP, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VOLT_CELL1, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VOLT_CELL2, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VOLT_CELL3, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VOLT_CELL4, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__BAT_TEMP1, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__BAT_TEMP2, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
            (resultInstance.a__int16__BAT_TEMP3, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 2)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 56
    
    class struct_EPS_4:
        def __init__(self, int16__VOLT_BRDSUP = 0, int16__TEMP_MCU = 0, int16__VIP_OUTPUT_Voltage = 0, int16__VIP_OUTPUT_Current = 0, int16__VIP_OUTPUT_Power = 0, a__int16__VIP_CC_OUTPUT_Voltage = [], a__int16__VIP_CC_OUTPUT_Current = [], a__int16__VIP_CC_OUTPUT_Power = [], a__int16__CCx_VOLT_IN_MPPT = [], a__int16__CCx_CURR_IN_MPPT = [], a__int16__CCx_VOLT_OU_MPPT = [], a__int16__CCx_CURR_OU_MPPT = []):
            self.int16__VOLT_BRDSUP = int16__VOLT_BRDSUP
            self.int16__TEMP_MCU = int16__TEMP_MCU
            self.int16__VIP_OUTPUT_Voltage = int16__VIP_OUTPUT_Voltage
            self.int16__VIP_OUTPUT_Current = int16__VIP_OUTPUT_Current
            self.int16__VIP_OUTPUT_Power = int16__VIP_OUTPUT_Power
            self.a__int16__VIP_CC_OUTPUT_Voltage = a__int16__VIP_CC_OUTPUT_Voltage
            self.a__int16__VIP_CC_OUTPUT_Current = a__int16__VIP_CC_OUTPUT_Current
            self.a__int16__VIP_CC_OUTPUT_Power = a__int16__VIP_CC_OUTPUT_Power
            self.a__int16__CCx_VOLT_IN_MPPT = a__int16__CCx_VOLT_IN_MPPT
            self.a__int16__CCx_CURR_IN_MPPT = a__int16__CCx_CURR_IN_MPPT
            self.a__int16__CCx_VOLT_OU_MPPT = a__int16__CCx_VOLT_OU_MPPT
            self.a__int16__CCx_CURR_OU_MPPT = a__int16__CCx_CURR_OU_MPPT
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VOLT_BRDSUP)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__TEMP_MCU)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_OUTPUT_Voltage)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_OUTPUT_Current)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__VIP_OUTPUT_Power)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VIP_CC_OUTPUT_Voltage)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VIP_CC_OUTPUT_Current)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__VIP_CC_OUTPUT_Power)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__CCx_VOLT_IN_MPPT)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__CCx_CURR_IN_MPPT)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__CCx_VOLT_OU_MPPT)
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__CCx_CURR_OU_MPPT)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_EPS_4()
    
            currentPos = pos
            (resultInstance.int16__VOLT_BRDSUP, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__TEMP_MCU, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_OUTPUT_Voltage, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_OUTPUT_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__VIP_OUTPUT_Power, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VIP_CC_OUTPUT_Voltage, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 4)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VIP_CC_OUTPUT_Current, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 4)
            currentPos += bytesProcessed
            (resultInstance.a__int16__VIP_CC_OUTPUT_Power, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 4)
            currentPos += bytesProcessed
            (resultInstance.a__int16__CCx_VOLT_IN_MPPT, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 4)
            currentPos += bytesProcessed
            (resultInstance.a__int16__CCx_CURR_IN_MPPT, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 4)
            currentPos += bytesProcessed
            (resultInstance.a__int16__CCx_VOLT_OU_MPPT, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 4)
            currentPos += bytesProcessed
            (resultInstance.a__int16__CCx_CURR_OU_MPPT, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 4)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 66
    
    class struct_EPS_5:
        def __init__(self, uint8__MODE = 0, uint8__RESET_CAUSE = 0, uint32__UPTIME = 0, uint16__ERROR = 0, uint16__RC_CNT_PWRON = 0, uint16__RC_CNT_WDG = 0, uint16__RC_CNT_CMD = 0, uint16__RC_CNT_MCU = 0, uint16__RC_CNT_EMLOPO = 0, uint32__UNIX_TIME = 0, uint32__UNIX_YEAR = 0, uint32__UNIX_MONTH = 0, uint32__UNIX_DAY = 0, uint32__UNIX_HOUR = 0, uint32__UNIX_MINUTE = 0, uint32__UNIX_SECOND = 0):
            self.uint8__MODE = uint8__MODE
            self.uint8__RESET_CAUSE = uint8__RESET_CAUSE
            self.uint32__UPTIME = uint32__UPTIME
            self.uint16__ERROR = uint16__ERROR
            self.uint16__RC_CNT_PWRON = uint16__RC_CNT_PWRON
            self.uint16__RC_CNT_WDG = uint16__RC_CNT_WDG
            self.uint16__RC_CNT_CMD = uint16__RC_CNT_CMD
            self.uint16__RC_CNT_MCU = uint16__RC_CNT_MCU
            self.uint16__RC_CNT_EMLOPO = uint16__RC_CNT_EMLOPO
            self.uint32__UNIX_TIME = uint32__UNIX_TIME
            self.uint32__UNIX_YEAR = uint32__UNIX_YEAR
            self.uint32__UNIX_MONTH = uint32__UNIX_MONTH
            self.uint32__UNIX_DAY = uint32__UNIX_DAY
            self.uint32__UNIX_HOUR = uint32__UNIX_HOUR
            self.uint32__UNIX_MINUTE = uint32__UNIX_MINUTE
            self.uint32__UNIX_SECOND = uint32__UNIX_SECOND
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__MODE)
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__RESET_CAUSE)
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__UPTIME)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__ERROR)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__RC_CNT_PWRON)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__RC_CNT_WDG)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__RC_CNT_CMD)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__RC_CNT_MCU)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__RC_CNT_EMLOPO)
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__UNIX_TIME)
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__UNIX_YEAR)
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__UNIX_MONTH)
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__UNIX_DAY)
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__UNIX_HOUR)
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__UNIX_MINUTE)
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__UNIX_SECOND)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_EPS_5()
    
            currentPos = pos
            (resultInstance.uint8__MODE, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint8__RESET_CAUSE, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint32__UPTIME, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__ERROR, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__RC_CNT_PWRON, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__RC_CNT_WDG, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__RC_CNT_CMD, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__RC_CNT_MCU, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__RC_CNT_EMLOPO, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint32__UNIX_TIME, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint32__UNIX_YEAR, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint32__UNIX_MONTH, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint32__UNIX_DAY, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint32__UNIX_HOUR, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint32__UNIX_MINUTE, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint32__UNIX_SECOND, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 46
    
    class struct_EPS_6:
        def __init__(self, uint16__STAT_CH_ON = 0, uint16__STAT_CH_OCF = 0, uint16__OCF_CNT_CH00 = 0, uint16__OCF_CNT_CH04 = 0, uint16__OCF_CNT_CH06 = 0, uint16__OCF_CNT_CH07 = 0, uint16__OCF_CNT_CH08 = 0, uint16__OCF_CNT_CH09 = 0, uint16__OCF_CNT_CH10 = 0, uint16__OCF_CNT_CH11 = 0):
            self.uint16__STAT_CH_ON = uint16__STAT_CH_ON
            self.uint16__STAT_CH_OCF = uint16__STAT_CH_OCF
            self.uint16__OCF_CNT_CH00 = uint16__OCF_CNT_CH00
            self.uint16__OCF_CNT_CH04 = uint16__OCF_CNT_CH04
            self.uint16__OCF_CNT_CH06 = uint16__OCF_CNT_CH06
            self.uint16__OCF_CNT_CH07 = uint16__OCF_CNT_CH07
            self.uint16__OCF_CNT_CH08 = uint16__OCF_CNT_CH08
            self.uint16__OCF_CNT_CH09 = uint16__OCF_CNT_CH09
            self.uint16__OCF_CNT_CH10 = uint16__OCF_CNT_CH10
            self.uint16__OCF_CNT_CH11 = uint16__OCF_CNT_CH11
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__STAT_CH_ON)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__STAT_CH_OCF)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__OCF_CNT_CH00)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__OCF_CNT_CH04)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__OCF_CNT_CH06)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__OCF_CNT_CH07)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__OCF_CNT_CH08)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__OCF_CNT_CH09)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__OCF_CNT_CH10)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__OCF_CNT_CH11)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_EPS_6()
    
            currentPos = pos
            (resultInstance.uint16__STAT_CH_ON, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__STAT_CH_OCF, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__OCF_CNT_CH00, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__OCF_CNT_CH04, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__OCF_CNT_CH06, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__OCF_CNT_CH07, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__OCF_CNT_CH08, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__OCF_CNT_CH09, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__OCF_CNT_CH10, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__OCF_CNT_CH11, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 20
    
    class struct_TaskStats:
        def __init__(self, a__int16__taskStackMaxUnusedSize = []):
            self.a__int16__taskStackMaxUnusedSize = a__int16__taskStackMaxUnusedSize
            
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__taskStackMaxUnusedSize)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_TaskStats()
    
            currentPos = pos
            (resultInstance.a__int16__taskStackMaxUnusedSize, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, dc_parser.NUM_TASKS)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return dc_parser.NUM_TASKS * 2
    
    class struct_SSP_3:
        def __init__(self, uint16__sunDataMain = 0, uint16__sunDataExt = 0, int16__tempMCU = 0, int16__tempMain = 0, int16__tempExt1 = 0, int16__tempExt2 = 0):
            self.uint16__sunDataMain = uint16__sunDataMain
            self.uint16__sunDataExt = uint16__sunDataExt
            self.int16__tempMCU = int16__tempMCU
            self.int16__tempMain = int16__tempMain
            self.int16__tempExt1 = int16__tempExt1
            self.int16__tempExt2 = int16__tempExt2
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__sunDataMain)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__sunDataExt)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempMCU)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempMain)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempExt1)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__tempExt2)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_SSP_3()
    
            currentPos = pos
            (resultInstance.uint16__sunDataMain, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__sunDataExt, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempMCU, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempMain, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempExt1, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__tempExt2, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_SENSOR_MAG_PRIMARY:
        def __init__(self, int32__MAG_X = 0, int32__MAG_Y = 0, int32__MAG_Z = 0):
            self.int32__MAG_X = int32__MAG_X
            self.int32__MAG_Y = int32__MAG_Y
            self.int32__MAG_Z = int32__MAG_Z
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_X)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Y)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Z)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_SENSOR_MAG_PRIMARY()
    
            currentPos = pos
            (resultInstance.int32__MAG_X, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Y, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Z, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_SENSOR_MAG_SECONDARY:
        def __init__(self, int32__MAG_X = 0, int32__MAG_Y = 0, int32__MAG_Z = 0):
            self.int32__MAG_X = int32__MAG_X
            self.int32__MAG_Y = int32__MAG_Y
            self.int32__MAG_Z = int32__MAG_Z
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_X)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Y)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Z)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_SENSOR_MAG_SECONDARY()
    
            currentPos = pos
            (resultInstance.int32__MAG_X, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Y, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Z, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_SENSOR_GYRO:
        def __init__(self, int32__GYRO_1 = 0, int32__GYRO_2 = 0, int32__GYRO_3 = 0):
            self.int32__GYRO_1 = int32__GYRO_1
            self.int32__GYRO_2 = int32__GYRO_2
            self.int32__GYRO_3 = int32__GYRO_3
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__GYRO_1)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__GYRO_2)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__GYRO_3)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_SENSOR_GYRO()
    
            currentPos = pos
            (resultInstance.int32__GYRO_1, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__GYRO_2, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__GYRO_3, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_SENSOR_COARSE_SUN:
        def __init__(self, int32__CSS_PANEL_1 = 0, int32__CSS_PANEL_2 = 0, int32__CSS_PANEL_3 = 0, int32__CSS_PANEL_4 = 0, int32__CSS_PANEL_5 = 0, int32__CSS_PANEL_6 = 0):
            self.int32__CSS_PANEL_1 = int32__CSS_PANEL_1
            self.int32__CSS_PANEL_2 = int32__CSS_PANEL_2
            self.int32__CSS_PANEL_3 = int32__CSS_PANEL_3
            self.int32__CSS_PANEL_4 = int32__CSS_PANEL_4
            self.int32__CSS_PANEL_5 = int32__CSS_PANEL_5
            self.int32__CSS_PANEL_6 = int32__CSS_PANEL_6
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_PANEL_1)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_PANEL_2)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_PANEL_3)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_PANEL_4)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_PANEL_5)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_PANEL_6)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_SENSOR_COARSE_SUN()
    
            currentPos = pos
            (resultInstance.int32__CSS_PANEL_1, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_PANEL_2, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_PANEL_3, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_PANEL_4, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_PANEL_5, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_PANEL_6, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 24
    
    class struct_ES_ADCS_SENSOR_MAG_PRIMARY:
        def __init__(self, int32__MAG_X_CURRENT = 0, int32__MAG_Y_CURRENT = 0, int32__MAG_Z_CURRENT = 0, int32__MAG_X_PREVIOUS = 0, int32__MAG_Y_PREVIOUS = 0, int32__MAG_Z_PREVIOUS = 0):
            self.int32__MAG_X_CURRENT = int32__MAG_X_CURRENT
            self.int32__MAG_Y_CURRENT = int32__MAG_Y_CURRENT
            self.int32__MAG_Z_CURRENT = int32__MAG_Z_CURRENT
            self.int32__MAG_X_PREVIOUS = int32__MAG_X_PREVIOUS
            self.int32__MAG_Y_PREVIOUS = int32__MAG_Y_PREVIOUS
            self.int32__MAG_Z_PREVIOUS = int32__MAG_Z_PREVIOUS
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_X_CURRENT)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Y_CURRENT)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Z_CURRENT)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_X_PREVIOUS)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Y_PREVIOUS)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Z_PREVIOUS)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ES_ADCS_SENSOR_MAG_PRIMARY()
    
            currentPos = pos
            (resultInstance.int32__MAG_X_CURRENT, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Y_CURRENT, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Z_CURRENT, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_X_PREVIOUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Y_PREVIOUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Z_PREVIOUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 24
    
    class struct_ES_ADCS_SENSOR_MAG_SECONDARY:
        def __init__(self, int32__MAG_X_CURRENT = 0, int32__MAG_Y_CURRENT = 0, int32__MAG_Z_CURRENT = 0, int32__MAG_X_PREVIOUS = 0, int32__MAG_Y_PREVIOUS = 0, int32__MAG_Z_PREVIOUS = 0):
            self.int32__MAG_X_CURRENT = int32__MAG_X_CURRENT
            self.int32__MAG_Y_CURRENT = int32__MAG_Y_CURRENT
            self.int32__MAG_Z_CURRENT = int32__MAG_Z_CURRENT
            self.int32__MAG_X_PREVIOUS = int32__MAG_X_PREVIOUS
            self.int32__MAG_Y_PREVIOUS = int32__MAG_Y_PREVIOUS
            self.int32__MAG_Z_PREVIOUS = int32__MAG_Z_PREVIOUS
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_X_CURRENT)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Y_CURRENT)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Z_CURRENT)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_X_PREVIOUS)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Y_PREVIOUS)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_Z_PREVIOUS)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ES_ADCS_SENSOR_MAG_SECONDARY()
    
            currentPos = pos
            (resultInstance.int32__MAG_X_CURRENT, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Y_CURRENT, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Z_CURRENT, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_X_PREVIOUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Y_PREVIOUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_Z_PREVIOUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 24
    
    class struct_ES_ADCS_SENSOR_GYRO:
        def __init__(self, int32__GYRO_X = 0, int32__GYRO_Y = 0, int32__GYRO_Z = 0):
            self.int32__GYRO_X = int32__GYRO_X
            self.int32__GYRO_Y = int32__GYRO_Y
            self.int32__GYRO_Z = int32__GYRO_Z
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__GYRO_X)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__GYRO_Y)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__GYRO_Z)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ES_ADCS_SENSOR_GYRO()
    
            currentPos = pos
            (resultInstance.int32__GYRO_X, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__GYRO_Y, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__GYRO_Z, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_ES_ADCS_SENSOR_CSS:
        def __init__(self, int32__CSS_AXIS_X_PLUS = 0, int32__CSS_AXIS_Y_PLUS = 0, int32__CSS_AXIS_Z_PLUS = 0, int32__CSS_AXIS_X_MINUS = 0, int32__CSS_AXIS_Y_MINUS = 0, int32__CSS_AXIS_Z_MINUS = 0):
            self.int32__CSS_AXIS_X_PLUS = int32__CSS_AXIS_X_PLUS
            self.int32__CSS_AXIS_Y_PLUS = int32__CSS_AXIS_Y_PLUS
            self.int32__CSS_AXIS_Z_PLUS = int32__CSS_AXIS_Z_PLUS
            self.int32__CSS_AXIS_X_MINUS = int32__CSS_AXIS_X_MINUS
            self.int32__CSS_AXIS_Y_MINUS = int32__CSS_AXIS_Y_MINUS
            self.int32__CSS_AXIS_Z_MINUS = int32__CSS_AXIS_Z_MINUS
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_AXIS_X_PLUS)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_AXIS_Y_PLUS)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_AXIS_Z_PLUS)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_AXIS_X_MINUS)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_AXIS_Y_MINUS)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__CSS_AXIS_Z_MINUS)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ES_ADCS_SENSOR_CSS()
    
            currentPos = pos
            (resultInstance.int32__CSS_AXIS_X_PLUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_AXIS_Y_PLUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_AXIS_Z_PLUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_AXIS_X_MINUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_AXIS_Y_MINUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__CSS_AXIS_Z_MINUS, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 24
    
    class struct_ES_ADCS_ESTIMATES_BDOT:
        def __init__(self, int32__MAG_FIELD_DERIV_X = 0, int32__MAG_FIELD_DERIV_Y = 0, int32__MAG_FIELD_DERIV_Z = 0):
            self.int32__MAG_FIELD_DERIV_X = int32__MAG_FIELD_DERIV_X
            self.int32__MAG_FIELD_DERIV_Y = int32__MAG_FIELD_DERIV_Y
            self.int32__MAG_FIELD_DERIV_Z = int32__MAG_FIELD_DERIV_Z
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_FIELD_DERIV_X)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_FIELD_DERIV_Y)
            result += SerDesHelpers.serdesType_basic.serialize("int32", self.int32__MAG_FIELD_DERIV_Z)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ES_ADCS_ESTIMATES_BDOT()
    
            currentPos = pos
            (resultInstance.int32__MAG_FIELD_DERIV_X, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_FIELD_DERIV_Y, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int32__MAG_FIELD_DERIV_Z, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int32", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_ES_ADCS_CONTROL_VALUES_MTQ:
        def __init__(self, int8__MAGTORQUE_VALUE_X = 0, int8__MAGTORQUE_VALUE_Y = 0, int8__MAGTORQUE_VALUE_Z = 0):
            self.int8__MAGTORQUE_VALUE_X = int8__MAGTORQUE_VALUE_X
            self.int8__MAGTORQUE_VALUE_Y = int8__MAGTORQUE_VALUE_Y
            self.int8__MAGTORQUE_VALUE_Z = int8__MAGTORQUE_VALUE_Z
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int8", self.int8__MAGTORQUE_VALUE_X)
            result += SerDesHelpers.serdesType_basic.serialize("int8", self.int8__MAGTORQUE_VALUE_Y)
            result += SerDesHelpers.serdesType_basic.serialize("int8", self.int8__MAGTORQUE_VALUE_Z)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ES_ADCS_CONTROL_VALUES_MTQ()
    
            currentPos = pos
            (resultInstance.int8__MAGTORQUE_VALUE_X, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int8", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int8__MAGTORQUE_VALUE_Y, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int8", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int8__MAGTORQUE_VALUE_Z, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int8", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 3
    
    class struct_ConOpsFlags:
        def __init__(self, bool__PAY_ERR = False, bool__ADCS_ERR = False, bool__DETUMB_COMPLETED = False):
            self.bool__PAY_ERR = bool__PAY_ERR
            self.bool__ADCS_ERR = bool__ADCS_ERR
            self.bool__DETUMB_COMPLETED = bool__DETUMB_COMPLETED
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.bool__PAY_ERR)
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.bool__ADCS_ERR)
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.bool__DETUMB_COMPLETED)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ConOpsFlags()
    
            currentPos = pos
            (resultInstance.bool__PAY_ERR, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.bool__ADCS_ERR, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.bool__DETUMB_COMPLETED, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 3
    
    class struct_AOCS_CNTRL_SYS_STATE:
        def __init__(self, uint8__adcsSysState = 0, uint8__adcsSysStateStatus = 0):
            self.uint8__adcsSysState = uint8__adcsSysState
            self.uint8__adcsSysStateStatus = uint8__adcsSysStateStatus
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__adcsSysState)
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__adcsSysStateStatus)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_AOCS_CNTRL_SYS_STATE()
    
            currentPos = pos
            (resultInstance.uint8__adcsSysState, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint8__adcsSysStateStatus, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 2
    
    class struct_ADCS_3:
        def __init__(self, int16__est_roll_angle = 0, int16__est_pitch_angle = 0, int16__est_yaw_angle = 0, int16__IGRF_MagField_X = 0, int16__IGRF_MagField_Y = 0, int16__IGRF_MagField_Z = 0, int16__Modelled_Sun_V_X = 0, int16__Modelled_Sun_V_Y = 0, int16__Modelled_Sun_V_Z = 0, int16__EstGyroBias_X = 0, int16__EstGyroBias_Y = 0, int16__EstGyroBias_Z = 0, int16__Innovation_Vec_X = 0, int16__Innovation_Vec_Y = 0, int16__Innovation_Vec_Z = 0, int16__Err_Q1 = 0, int16__Err_Q2 = 0, int16__Err_Q3 = 0, int16__RMS_Q1 = 0, int16__RMS_Q2 = 0, int16__RMS_Q3 = 0, int16__X_AngRate_Cov = 0, int16__Y_AngRate_Cov = 0, int16__Z_AngRate_Cov = 0, int16__X_Rate = 0, int16__Y_Rate = 0, int16__Z_Rate = 0, int16__Q0 = 0, int16__Q1 = 0, int16__Q2 = 0):
            self.int16__est_roll_angle = int16__est_roll_angle
            self.int16__est_pitch_angle = int16__est_pitch_angle
            self.int16__est_yaw_angle = int16__est_yaw_angle
            self.int16__IGRF_MagField_X = int16__IGRF_MagField_X
            self.int16__IGRF_MagField_Y = int16__IGRF_MagField_Y
            self.int16__IGRF_MagField_Z = int16__IGRF_MagField_Z
            self.int16__Modelled_Sun_V_X = int16__Modelled_Sun_V_X
            self.int16__Modelled_Sun_V_Y = int16__Modelled_Sun_V_Y
            self.int16__Modelled_Sun_V_Z = int16__Modelled_Sun_V_Z
            self.int16__EstGyroBias_X = int16__EstGyroBias_X
            self.int16__EstGyroBias_Y = int16__EstGyroBias_Y
            self.int16__EstGyroBias_Z = int16__EstGyroBias_Z
            self.int16__Innovation_Vec_X = int16__Innovation_Vec_X
            self.int16__Innovation_Vec_Y = int16__Innovation_Vec_Y
            self.int16__Innovation_Vec_Z = int16__Innovation_Vec_Z
            self.int16__Err_Q1 = int16__Err_Q1
            self.int16__Err_Q2 = int16__Err_Q2
            self.int16__Err_Q3 = int16__Err_Q3
            self.int16__RMS_Q1 = int16__RMS_Q1
            self.int16__RMS_Q2 = int16__RMS_Q2
            self.int16__RMS_Q3 = int16__RMS_Q3
            self.int16__X_AngRate_Cov = int16__X_AngRate_Cov
            self.int16__Y_AngRate_Cov = int16__Y_AngRate_Cov
            self.int16__Z_AngRate_Cov = int16__Z_AngRate_Cov
            self.int16__X_Rate = int16__X_Rate
            self.int16__Y_Rate = int16__Y_Rate
            self.int16__Z_Rate = int16__Z_Rate
            self.int16__Q0 = int16__Q0
            self.int16__Q1 = int16__Q1
            self.int16__Q2 = int16__Q2
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__est_roll_angle)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__est_pitch_angle)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__est_yaw_angle)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__IGRF_MagField_X)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__IGRF_MagField_Y)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__IGRF_MagField_Z)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Modelled_Sun_V_X)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Modelled_Sun_V_Y)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Modelled_Sun_V_Z)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__EstGyroBias_X)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__EstGyroBias_Y)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__EstGyroBias_Z)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Innovation_Vec_X)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Innovation_Vec_Y)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Innovation_Vec_Z)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Err_Q1)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Err_Q2)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Err_Q3)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__RMS_Q1)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__RMS_Q2)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__RMS_Q3)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__X_AngRate_Cov)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Y_AngRate_Cov)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Z_AngRate_Cov)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__X_Rate)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Y_Rate)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Z_Rate)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Q0)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Q1)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Q2)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ADCS_3()
    
            currentPos = pos
            (resultInstance.int16__est_roll_angle, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__est_pitch_angle, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__est_yaw_angle, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__IGRF_MagField_X, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__IGRF_MagField_Y, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__IGRF_MagField_Z, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Modelled_Sun_V_X, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Modelled_Sun_V_Y, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Modelled_Sun_V_Z, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__EstGyroBias_X, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__EstGyroBias_Y, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__EstGyroBias_Z, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Innovation_Vec_X, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Innovation_Vec_Y, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Innovation_Vec_Z, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Err_Q1, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Err_Q2, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Err_Q3, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__RMS_Q1, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__RMS_Q2, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__RMS_Q3, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__X_AngRate_Cov, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Y_AngRate_Cov, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Z_AngRate_Cov, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__X_Rate, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Y_Rate, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Z_Rate, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Q0, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Q1, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Q2, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 60
    
    class struct_ADCS_4:
        def __init__(self, uint16__Cubesense1_3V3_Current = 0, uint16__Cubesense1_SRAM_Current = 0, uint16__Cubesense2_3V3_Current = 0, uint16__Cubesense2_SRAM_Current = 0, uint16__CubeControl_3V3_Current = 0, uint16__CubeControl_5V_Current = 0, uint16__CubeControl_Vbat_Current = 0, uint16__Wheel_1_Current = 0, uint16__Wheel_2_Current = 0, uint16__Wheel_3_Current = 0, uint16__CubeStar_Current = 0, uint16__MTQ_Current = 0, int16__CubeStar_MCU_Temp = 0, int16__ADCS_MCU_Temp = 0, int16__MTM_Temp = 0, int16__RMTM_Temp = 0, int16__X_Rate_Sensor_Temp = 0, int16__Y_Rate_Sensor_Temp = 0, int16__Z_Rate_Sensor_Temp = 0):
            self.uint16__Cubesense1_3V3_Current = uint16__Cubesense1_3V3_Current
            self.uint16__Cubesense1_SRAM_Current = uint16__Cubesense1_SRAM_Current
            self.uint16__Cubesense2_3V3_Current = uint16__Cubesense2_3V3_Current
            self.uint16__Cubesense2_SRAM_Current = uint16__Cubesense2_SRAM_Current
            self.uint16__CubeControl_3V3_Current = uint16__CubeControl_3V3_Current
            self.uint16__CubeControl_5V_Current = uint16__CubeControl_5V_Current
            self.uint16__CubeControl_Vbat_Current = uint16__CubeControl_Vbat_Current
            self.uint16__Wheel_1_Current = uint16__Wheel_1_Current
            self.uint16__Wheel_2_Current = uint16__Wheel_2_Current
            self.uint16__Wheel_3_Current = uint16__Wheel_3_Current
            self.uint16__CubeStar_Current = uint16__CubeStar_Current
            self.uint16__MTQ_Current = uint16__MTQ_Current
            self.int16__CubeStar_MCU_Temp = int16__CubeStar_MCU_Temp
            self.int16__ADCS_MCU_Temp = int16__ADCS_MCU_Temp
            self.int16__MTM_Temp = int16__MTM_Temp
            self.int16__RMTM_Temp = int16__RMTM_Temp
            self.int16__X_Rate_Sensor_Temp = int16__X_Rate_Sensor_Temp
            self.int16__Y_Rate_Sensor_Temp = int16__Y_Rate_Sensor_Temp
            self.int16__Z_Rate_Sensor_Temp = int16__Z_Rate_Sensor_Temp
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__Cubesense1_3V3_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__Cubesense1_SRAM_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__Cubesense2_3V3_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__Cubesense2_SRAM_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__CubeControl_3V3_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__CubeControl_5V_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__CubeControl_Vbat_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__Wheel_1_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__Wheel_2_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__Wheel_3_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__CubeStar_Current)
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__MTQ_Current)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__CubeStar_MCU_Temp)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__ADCS_MCU_Temp)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__MTM_Temp)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__RMTM_Temp)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__X_Rate_Sensor_Temp)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Y_Rate_Sensor_Temp)
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__Z_Rate_Sensor_Temp)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = dc_parser.struct_ADCS_4()
    
            currentPos = pos
            (resultInstance.uint16__Cubesense1_3V3_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__Cubesense1_SRAM_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__Cubesense2_3V3_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__Cubesense2_SRAM_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__CubeControl_3V3_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__CubeControl_5V_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__CubeControl_Vbat_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__Wheel_1_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__Wheel_2_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__Wheel_3_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__CubeStar_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.uint16__MTQ_Current, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__CubeStar_MCU_Temp, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__ADCS_MCU_Temp, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__MTM_Temp, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__RMTM_Temp, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__X_Rate_Sensor_Temp, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Y_Rate_Sensor_Temp, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            (resultInstance.int16__Z_Rate_Sensor_Temp, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 38
    
