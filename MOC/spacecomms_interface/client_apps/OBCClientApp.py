# ********************************************************************************************
# * @file OBCClientApp.py
# * @brief MAC FP client Python implementation generator
# ********************************************************************************************
# * @version           interface OBC v2.0
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

from .SerDesHelpers import SerDesHelpers

class FP_API_OBC:
    def __init__(self, rawSerDesSupport : bool = False):
        self.const_OBC_PROTOCOL_ID = 14
        self.rawSerDesSupport = rawSerDesSupport
        self.versionMajor=2
        self.versionMinor=0


        #
        # Response parsers map
        #
        self.responseParsersDict = {}
        self.responseParsersDict[0] = self.resp_getAccelerationData
        self.responseParsersDict[1] = self.resp_readAccelerometerRegister
        self.responseParsersDict[2] = self.resp_updateAccelerometerRegister
        self.responseParsersDict[3] = self.resp_getMagnetometerData
        self.responseParsersDict[4] = self.resp_readMagnetometerRegister
        self.responseParsersDict[5] = self.resp_updateMagnetometerRegister
        self.responseParsersDict[6] = self.resp_readGyroMetricData
        self.responseParsersDict[7] = self.resp_readGyroAngleDisplacementData
        self.responseParsersDict[8] = self.resp_readGyroRegister
        self.responseParsersDict[9] = self.resp_updateGyroRegister
        self.responseParsersDict[10] = self.resp_readMagnetorquerData
        self.responseParsersDict[11] = self.resp_applyMagnetorquerData
        self.responseParsersDict[12] = self.resp_readTemperatureData
        self.responseParsersDict[13] = self.resp_getPhotometricInfo
        self.responseParsersDict[14] = self.resp_getGpOutputStates
        self.responseParsersDict[15] = self.resp_setGpOutputState
        self.responseParsersDict[16] = self.resp_getSensorsInUse
        self.responseParsersDict[17] = self.resp_triggerSensorCommand
        self.responseParsersDict[18] = self.resp_getI2CPullUpsState
        self.responseParsersDict[19] = self.resp_setI2CPullUpsState
        self.responseParsersDict[24] = self.resp_getUptime
        self.responseParsersDict[42] = self.resp_getResetCounters
        self.responseParsersDict[43] = self.resp_clearResetCounter
        self.responseParsersDict[54] = self.resp_triggerResetInMode
        self.responseParsersDict[63] = self.resp_triggerFwUpdate

    class enum_HwResult:
        HWRESULT_SUCCESS = 0
        HWRESULT_ERROR = 1
        HWRESULT_DISABLED = 255
    
        ValuesDict = {
            HWRESULT_SUCCESS : 'HWRESULT_SUCCESS', 
            HWRESULT_ERROR : 'HWRESULT_ERROR', 
            HWRESULT_DISABLED : 'HWRESULT_DISABLED'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_HwResult()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_HwResult.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_HwResult.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class enum_StandardResult:
        STANDARDRESULT_SUCCESS = 0
        STANDARDRESULT_ERROR = 1
        STANDARDRESULT_INVALID_ARGS = 2
        STANDARDRESULT_NOT_SUPPORTED = 3
    
        ValuesDict = {
            STANDARDRESULT_SUCCESS : 'STANDARDRESULT_SUCCESS', 
            STANDARDRESULT_ERROR : 'STANDARDRESULT_ERROR', 
            STANDARDRESULT_INVALID_ARGS : 'STANDARDRESULT_INVALID_ARGS', 
            STANDARDRESULT_NOT_SUPPORTED : 'STANDARDRESULT_NOT_SUPPORTED'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_StandardResult()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_StandardResult.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_StandardResult.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class enum_ApplicationMode:
        APPLICATIONMODE_APPLICATION = 0
        APPLICATIONMODE_BOOTLOADER = 1
    
        ValuesDict = {
            APPLICATIONMODE_APPLICATION : 'APPLICATIONMODE_APPLICATION', 
            APPLICATIONMODE_BOOTLOADER : 'APPLICATIONMODE_BOOTLOADER'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_ApplicationMode()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_ApplicationMode.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_ApplicationMode.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class struct_PanelPhotometricInfo:
        def __init__(self, a__uint16__6__sensorReadings = []):
            self.a__uint16__6__sensorReadings = a__uint16__6__sensorReadings
    
        def serialize(self):
            result = bytearray()
    
            actualLen = len(self.a__uint16__6__sensorReadings)
            
            result += SerDesHelpers.serdesType_basicArray.serialize("uint16", self.a__uint16__6__sensorReadings, 6)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_PanelPhotometricInfo()
    
            currentPos = pos
            
            (resultInstance.a__uint16__6__sensorReadings, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("uint16", data, currentPos, 6)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 12
    
    class struct_GpioStatus:
        def __init__(self, uint8__gpioStatusBitField = 0):
            self.uint8__gpioStatusBitField = uint8__gpioStatusBitField
    
        def serialize(self):
            result = bytearray()
    
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__gpioStatusBitField)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_GpioStatus()
    
            currentPos = pos
            
            (resultInstance.uint8__gpioStatusBitField, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 1
    
    class enum_ObcSensor:
        OBCSENSOR_ACCELEROMETER = 0
        OBCSENSOR_MAGNETOMETER = 1
        OBCSENSOR_GYROSCOPE = 2
        OBCSENSOR_MAGNETORQUER = 3
        OBCSENSOR_TEMPERATURE_SENSOR = 4
        OBCSENSOR_SUN_SENSOR = 5
    
        ValuesDict = {
            OBCSENSOR_ACCELEROMETER : 'OBCSENSOR_ACCELEROMETER', 
            OBCSENSOR_MAGNETOMETER : 'OBCSENSOR_MAGNETOMETER', 
            OBCSENSOR_GYROSCOPE : 'OBCSENSOR_GYROSCOPE', 
            OBCSENSOR_MAGNETORQUER : 'OBCSENSOR_MAGNETORQUER', 
            OBCSENSOR_TEMPERATURE_SENSOR : 'OBCSENSOR_TEMPERATURE_SENSOR', 
            OBCSENSOR_SUN_SENSOR : 'OBCSENSOR_SUN_SENSOR'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_ObcSensor()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_ObcSensor.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_ObcSensor.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class enum_ObcSensorCmd:
        OBCSENSORCMD_RELEASE_FOR_ONE_USER = 0
        OBCSENSORCMD_RESERVE_FOR_ONE_USER = 1
        OBCSENSORCMD_RELEASE_FOR_ALL_AND_OFF = 90
    
        ValuesDict = {
            OBCSENSORCMD_RELEASE_FOR_ONE_USER : 'OBCSENSORCMD_RELEASE_FOR_ONE_USER', 
            OBCSENSORCMD_RESERVE_FOR_ONE_USER : 'OBCSENSORCMD_RESERVE_FOR_ONE_USER', 
            OBCSENSORCMD_RELEASE_FOR_ALL_AND_OFF : 'OBCSENSORCMD_RELEASE_FOR_ALL_AND_OFF'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_ObcSensorCmd()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_ObcSensorCmd.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_ObcSensorCmd.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class struct_I2CPullUpsState:
        def __init__(self, bool__SystemBus_4K7 = False, bool__SystemBus_10K = False, bool__PayloadBus_4K7 = False, bool__PayloadBus_10K = False):
            self.bool__SystemBus_4K7 = bool__SystemBus_4K7
            self.bool__SystemBus_10K = bool__SystemBus_10K
            self.bool__PayloadBus_4K7 = bool__PayloadBus_4K7
            self.bool__PayloadBus_10K = bool__PayloadBus_10K
    
        def serialize(self):
            result = bytearray()
    
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.bool__SystemBus_4K7)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.bool__SystemBus_10K)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.bool__PayloadBus_4K7)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.bool__PayloadBus_10K)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_I2CPullUpsState()
    
            currentPos = pos
            
            (resultInstance.bool__SystemBus_4K7, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.bool__SystemBus_10K, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.bool__PayloadBus_4K7, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.bool__PayloadBus_10K, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 4
    
    class struct_UptimeInfo:
        def __init__(self, uint32__days = 0, uint8__hours = 0, uint8__minutes = 0, uint8__seconds = 0):
            self.uint32__days = uint32__days
            self.uint8__hours = uint8__hours
            self.uint8__minutes = uint8__minutes
            self.uint8__seconds = uint8__seconds
    
        def serialize(self):
            result = bytearray()
    
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__days)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__hours)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__minutes)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__seconds)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_UptimeInfo()
    
            currentPos = pos
            
            (resultInstance.uint32__days, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint8__hours, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint8__minutes, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint8__seconds, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 7
    
    class struct_ResetCountersInfo:
        def __init__(self, uint32__WWD = 0, uint32__IWD = 0, uint32__LPR = 0, uint32__POR = 0, uint32__RstPin = 0, uint32__BOR = 0, uint32__HardFault = 0, uint32__MemFault = 0, uint32__BusFault = 0, uint32__UsageFault = 0):
            self.uint32__WWD = uint32__WWD
            self.uint32__IWD = uint32__IWD
            self.uint32__LPR = uint32__LPR
            self.uint32__POR = uint32__POR
            self.uint32__RstPin = uint32__RstPin
            self.uint32__BOR = uint32__BOR
            self.uint32__HardFault = uint32__HardFault
            self.uint32__MemFault = uint32__MemFault
            self.uint32__BusFault = uint32__BusFault
            self.uint32__UsageFault = uint32__UsageFault
    
        def serialize(self):
            result = bytearray()
    
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__WWD)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__IWD)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__LPR)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__POR)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__RstPin)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__BOR)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__HardFault)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__MemFault)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__BusFault)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint32", self.uint32__UsageFault)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_ResetCountersInfo()
    
            currentPos = pos
            
            (resultInstance.uint32__WWD, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint32__IWD, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint32__LPR, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint32__POR, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint32__RstPin, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint32__BOR, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint32__HardFault, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint32__MemFault, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint32__BusFault, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint32__UsageFault, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint32", data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 40
    
    class enum_ResetCntrId:
        RESETCNTRID_WWD = 0
        RESETCNTRID_IWD = 1
        RESETCNTRID_LPR = 2
        RESETCNTRID_POR = 3
        RESETCNTRID_RSTPIN = 4
        RESETCNTRID_BOR = 5
        RESETCNTRID_HARDFAULT = 6
        RESETCNTRID_MEMFAULT = 7
        RESETCNTRID_BUSFAULT = 8
        RESETCNTRID_USAGEFAULT = 9
        RESETCNTRID_ALL = 10
    
        ValuesDict = {
            RESETCNTRID_WWD : 'RESETCNTRID_WWD', 
            RESETCNTRID_IWD : 'RESETCNTRID_IWD', 
            RESETCNTRID_LPR : 'RESETCNTRID_LPR', 
            RESETCNTRID_POR : 'RESETCNTRID_POR', 
            RESETCNTRID_RSTPIN : 'RESETCNTRID_RSTPIN', 
            RESETCNTRID_BOR : 'RESETCNTRID_BOR', 
            RESETCNTRID_HARDFAULT : 'RESETCNTRID_HARDFAULT', 
            RESETCNTRID_MEMFAULT : 'RESETCNTRID_MEMFAULT', 
            RESETCNTRID_BUSFAULT : 'RESETCNTRID_BUSFAULT', 
            RESETCNTRID_USAGEFAULT : 'RESETCNTRID_USAGEFAULT', 
            RESETCNTRID_ALL : 'RESETCNTRID_ALL'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_ResetCntrId()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_ResetCntrId.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_ResetCntrId.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class struct_TemperatureInfo:
        def __init__(self, a__e__HwResult__6__status = [], a__int16__6__rawData = [], a__int16__6__degCData = []):
            self.a__e__HwResult__6__status = a__e__HwResult__6__status
            self.a__int16__6__rawData = a__int16__6__rawData
            self.a__int16__6__degCData = a__int16__6__degCData
    
        def serialize(self):
            result = bytearray()
    
            
            result += SerDesHelpers.serdesType_customTypeArray.serialize(self.a__e__HwResult__6__status, 6)
            actualLen = len(self.a__int16__6__rawData)
            
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__6__rawData, 6)
            actualLen = len(self.a__int16__6__degCData)
            
            result += SerDesHelpers.serdesType_basicArray.serialize("int16", self.a__int16__6__degCData, 6)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_TemperatureInfo()
    
            currentPos = pos
            
            (resultInstance.a__e__HwResult__6__status, bytesProcessed) = SerDesHelpers.serdesType_customTypeArray.deserialize(FP_API_OBC.enum_HwResult, data, currentPos, 6)
            currentPos += bytesProcessed
            
            
            (resultInstance.a__int16__6__rawData, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 6)
            currentPos += bytesProcessed
            
            
            (resultInstance.a__int16__6__degCData, bytesProcessed) = SerDesHelpers.serdesType_basicArray.deserialize("int16", data, currentPos, 6)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 30
    
    class struct_MagnetorquerInfo:
        def __init__(self, e__HwResult__status = 0, uint8__power = 0, uint8__direction = 0, uint8__usersCount = 0):
            self.e__HwResult__status = e__HwResult__status
            self.uint8__power = uint8__power
            self.uint8__direction = uint8__direction
            self.uint8__usersCount = uint8__usersCount
    
        def serialize(self):
            result = bytearray()
    
            
            result += FP_API_OBC.enum_HwResult(self.e__HwResult__status).serialize()
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__power)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__direction)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__usersCount)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_MagnetorquerInfo()
    
            currentPos = pos
            
            (resultInstance.e__HwResult__status, bytesProcessed) = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint8__power, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint8__direction, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint8__usersCount, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 4
    
    class enum_PanelId:
        PANELID_X_P = 0
        PANELID_Y_P = 1
        PANELID_Z_P = 2
        PANELID_X_M = 3
        PANELID_Y_M = 4
        PANELID_Z_M = 5
    
        ValuesDict = {
            PANELID_X_P : 'PANELID_X_P', 
            PANELID_Y_P : 'PANELID_Y_P', 
            PANELID_Z_P : 'PANELID_Z_P', 
            PANELID_X_M : 'PANELID_X_M', 
            PANELID_Y_M : 'PANELID_Y_M', 
            PANELID_Z_M : 'PANELID_Z_M'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_PanelId()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_PanelId.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_PanelId.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class enum_AxisId:
        AXISID_X = 0
        AXISID_Y = 1
        AXISID_Z = 2
    
        ValuesDict = {
            AXISID_X : 'AXISID_X', 
            AXISID_Y : 'AXISID_Y', 
            AXISID_Z : 'AXISID_Z'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_AxisId()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_AxisId.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_AxisId.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class struct_GyroAxisData:
        def __init__(self, e__HwResult__status = 0, int16__data = 0):
            self.e__HwResult__status = e__HwResult__status
            self.int16__data = int16__data
    
        def serialize(self):
            result = bytearray()
    
            
            result += FP_API_OBC.enum_HwResult(self.e__HwResult__status).serialize()
            
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__data)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_GyroAxisData()
    
            currentPos = pos
            
            (resultInstance.e__HwResult__status, bytesProcessed) = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.int16__data, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 3
    
    class enum_MagnetometerId:
        MAGNETOMETERID_LOW = 0
        MAGNETOMETERID_HIGH = 1
    
        ValuesDict = {
            MAGNETOMETERID_LOW : 'MAGNETOMETERID_LOW', 
            MAGNETOMETERID_HIGH : 'MAGNETOMETERID_HIGH'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_MagnetometerId()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_MagnetometerId.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_MagnetometerId.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class struct_MagnXYZData:
        def __init__(self, double__MagnX = 0.0, double__MagnY = 0.0, double__MagnZ = 0.0):
            self.double__MagnX = double__MagnX
            self.double__MagnY = double__MagnY
            self.double__MagnZ = double__MagnZ
    
        def serialize(self):
            result = bytearray()
    
            
            result += SerDesHelpers.serdesType_double.serialize(self.double__MagnX)
            
            result += SerDesHelpers.serdesType_double.serialize(self.double__MagnY)
            
            result += SerDesHelpers.serdesType_double.serialize(self.double__MagnZ)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_MagnXYZData()
    
            currentPos = pos
            
            (resultInstance.double__MagnX, bytesProcessed) = SerDesHelpers.serdesType_double.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.double__MagnY, bytesProcessed) = SerDesHelpers.serdesType_double.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.double__MagnZ, bytesProcessed) = SerDesHelpers.serdesType_double.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 24
    
    class struct_MagnXYZExtData:
        def __init__(self, e__HwResult__status = 0, s__data = None):
            self.e__HwResult__status = e__HwResult__status
            self.s__data = s__data
    
        def serialize(self):
            result = bytearray()
    
            
            result += FP_API_OBC.enum_HwResult(self.e__HwResult__status).serialize()
            
            result += self.s__data.serialize()
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_MagnXYZExtData()
    
            currentPos = pos
            
            (resultInstance.e__HwResult__status, bytesProcessed) = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.s__data, bytesProcessed) = FP_API_OBC.struct_MagnXYZData.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 25
    
    class struct_AccelXYZData:
        def __init__(self, int16__AccelX = 0, int16__AccelY = 0, int16__AccelZ = 0):
            self.int16__AccelX = int16__AccelX
            self.int16__AccelY = int16__AccelY
            self.int16__AccelZ = int16__AccelZ
    
        def serialize(self):
            result = bytearray()
    
            
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__AccelX)
            
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__AccelY)
            
            result += SerDesHelpers.serdesType_basic.serialize("int16", self.int16__AccelZ)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_AccelXYZData()
    
            currentPos = pos
            
            (resultInstance.int16__AccelX, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.int16__AccelY, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.int16__AccelZ, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("int16", data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 6
    
    class struct_AccelXYZExtData:
        def __init__(self, e__HwResult__status = 0, s__data = None):
            self.e__HwResult__status = e__HwResult__status
            self.s__data = s__data
    
        def serialize(self):
            result = bytearray()
    
            
            result += FP_API_OBC.enum_HwResult(self.e__HwResult__status).serialize()
            
            result += self.s__data.serialize()
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_AccelXYZExtData()
    
            currentPos = pos
            
            (resultInstance.e__HwResult__status, bytesProcessed) = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.s__data, bytesProcessed) = FP_API_OBC.struct_AccelXYZData.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 7
    
    class enum_AccelId:
        ACCELID_ONE = 0
        ACCELID_TWO = 1
    
        ValuesDict = {
            ACCELID_ONE : 'ACCELID_ONE', 
            ACCELID_TWO : 'ACCELID_TWO'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_AccelId()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_AccelId.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_AccelId.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    
    class struct_RegData:
        def __init__(self, e__HwResult__status = 0, uint16__data = 0):
            self.e__HwResult__status = e__HwResult__status
            self.uint16__data = uint16__data
    
        def serialize(self):
            result = bytearray()
    
            
            result += FP_API_OBC.enum_HwResult(self.e__HwResult__status).serialize()
            
            result += SerDesHelpers.serdesType_basic.serialize("uint16", self.uint16__data)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_RegData()
    
            currentPos = pos
            
            (resultInstance.e__HwResult__status, bytesProcessed) = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint16__data, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint16", data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 3
    
    class struct_SensorInUseData:
        def __init__(self, bool__isSensorValid = False, uint8__usersCount = 0):
            self.bool__isSensorValid = bool__isSensorValid
            self.uint8__usersCount = uint8__usersCount
    
        def serialize(self):
            result = bytearray()
    
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.bool__isSensorValid)
            
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.uint8__usersCount)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.struct_SensorInUseData()
    
            currentPos = pos
            
            (resultInstance.bool__isSensorValid, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
            
            (resultInstance.uint8__usersCount, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, currentPos)
            currentPos += bytesProcessed
            
    
            # tuple[1] shall contain the total number of bytes processed by the function
            return (resultInstance, currentPos - pos)
    
        @staticmethod
        def getSize():
            return 2
    
    class enum_SafeBool:
        SAFEBOOL_FALSE = 0
        SAFEBOOL_TRUE = 255
    
        ValuesDict = {
            SAFEBOOL_FALSE : 'SAFEBOOL_FALSE', 
            SAFEBOOL_TRUE : 'SAFEBOOL_TRUE'
        }
    
        def __init__(self, value = 0):
            self.value = value
    
        def serialize(self):
            result = bytearray()
    
            result += SerDesHelpers.serdesType_basic.serialize("uint8", self.value)
    
            return result
    
        @staticmethod
        def deserialize(data, pos):
            resultInstance = FP_API_OBC.enum_SafeBool()
    
            (resultInstance.value, bytesProcessed) = SerDesHelpers.serdesType_basic.deserialize("uint8", data, pos)
    
            return (resultInstance, bytesProcessed)
    
        def getSymbolicName(self):
            return FP_API_OBC.enum_SafeBool.ValuesDict[self.value]
    
        @staticmethod
        def getValueBySymbolicName(literalName):
            for key, value in FP_API_OBC.enum_SafeBool.ValuesDict.items():
                if literalName == value:
                    return key
    
        @staticmethod
        def getSize():
            return 1
    

    ############################################################################################################
    """
    Request function for FIDL method: getAccelerationData
        - function ID: 00000000
        - description: Provides the raw acceleration data per axis for a given accelerometer
    """
    def req_getAccelerationData(self, e__AccelId__id):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000000
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_AccelId(e__AccelId__id).serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000000, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: getAccelerationData
        - function ID: 00000000
        - description: Provides the raw acceleration data per axis for a given accelerometer
    """
    def resp_getAccelerationData(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000000):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_AccelXYZExtData.deserialize(data, currentPos)
        responseInstance["s__accelData"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: readAccelerometerRegister
        - function ID: 00000001
        - description: Reads the value of a given accelerometer register
    """
    def req_readAccelerometerRegister(self, e__AccelId__id, uint8__regAddr):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000001
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_AccelId(e__AccelId__id).serialize()
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__regAddr)
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000001, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: readAccelerometerRegister
        - function ID: 00000001
        - description: Reads the value of a given accelerometer register
    """
    def resp_readAccelerometerRegister(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000001):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_RegData.deserialize(data, currentPos)
        responseInstance["s__regData"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: updateAccelerometerRegister
        - function ID: 00000002
        - description: Updates the value of a given accelerometer register. Please note that there is no internal protection which
                              stops you from writing to reserved (do-not-modify) registers. This functionality is provided for HW testing of
                              different accelerometer settings.
    """
    def req_updateAccelerometerRegister(self, e__AccelId__id, uint8__regAddr, uint8__regValue):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000002
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_AccelId(e__AccelId__id).serialize()
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__regAddr)
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__regValue)
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000002, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: updateAccelerometerRegister
        - function ID: 00000002
        - description: Updates the value of a given accelerometer register. Please note that there is no internal protection which
                              stops you from writing to reserved (do-not-modify) registers. This functionality is provided for HW testing of
                              different accelerometer settings.
    """
    def resp_updateAccelerometerRegister(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000002):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
        responseInstance["e__HwResult__status"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: getMagnetometerData
        - function ID: 00000003
        - description: Provides the raw magnetic field data per axis for a given magnetometer
    """
    def req_getMagnetometerData(self, e__MagnetometerId__id):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000003
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_MagnetometerId(e__MagnetometerId__id).serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000003, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: getMagnetometerData
        - function ID: 00000003
        - description: Provides the raw magnetic field data per axis for a given magnetometer
    """
    def resp_getMagnetometerData(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000003):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_MagnXYZExtData.deserialize(data, currentPos)
        responseInstance["s__magnData"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: readMagnetometerRegister
        - function ID: 00000004
        - description: Reads the value of a given magnetometer register
    """
    def req_readMagnetometerRegister(self, e__MagnetometerId__id, uint8__regAddr):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000004
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_MagnetometerId(e__MagnetometerId__id).serialize()
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__regAddr)
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000004, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: readMagnetometerRegister
        - function ID: 00000004
        - description: Reads the value of a given magnetometer register
    """
    def resp_readMagnetometerRegister(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000004):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_RegData.deserialize(data, currentPos)
        responseInstance["s__regData"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: updateMagnetometerRegister
        - function ID: 00000005
        - description: Updates the value of a given magnetometer register
    """
    def req_updateMagnetometerRegister(self, e__MagnetometerId__id, uint8__regAddr, uint8__regValue):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000005
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_MagnetometerId(e__MagnetometerId__id).serialize()
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__regAddr)
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__regValue)
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000005, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: updateMagnetometerRegister
        - function ID: 00000005
        - description: Updates the value of a given magnetometer register
    """
    def resp_updateMagnetometerRegister(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000005):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
        responseInstance["e__HwResult__status"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: readGyroMetricData
        - function ID: 00000006
        - description: Reads the gyroscope metric data for a given axis
    """
    def req_readGyroMetricData(self, e__AxisId__axis):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000006
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_AxisId(e__AxisId__axis).serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000006, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: readGyroMetricData
        - function ID: 00000006
        - description: Reads the gyroscope metric data for a given axis
    """
    def resp_readGyroMetricData(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000006):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_GyroAxisData.deserialize(data, currentPos)
        responseInstance["s__regData"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: readGyroAngleDisplacementData
        - function ID: 00000007
        - description: Reads the gyroscope angle displacement data for a given axis
    """
    def req_readGyroAngleDisplacementData(self, e__AxisId__axis):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000007
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_AxisId(e__AxisId__axis).serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000007, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: readGyroAngleDisplacementData
        - function ID: 00000007
        - description: Reads the gyroscope angle displacement data for a given axis
    """
    def resp_readGyroAngleDisplacementData(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000007):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_GyroAxisData.deserialize(data, currentPos)
        responseInstance["s__regData"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: readGyroRegister
        - function ID: 00000008
        - description: Reads the value of a given gyroscope register
    """
    def req_readGyroRegister(self, e__PanelId__id, uint8__regAddr):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000008
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_PanelId(e__PanelId__id).serialize()
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__regAddr)
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000008, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: readGyroRegister
        - function ID: 00000008
        - description: Reads the value of a given gyroscope register
    """
    def resp_readGyroRegister(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000008):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_RegData.deserialize(data, currentPos)
        responseInstance["s__regData"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: updateGyroRegister
        - function ID: 00000009
        - description: Updates the value of a given gyroscope register
    """
    def req_updateGyroRegister(self, e__PanelId__id, uint8__regAddr, uint16__regValue):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000009
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_PanelId(e__PanelId__id).serialize()
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__regAddr)
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint16", uint16__regValue)
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000009, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: updateGyroRegister
        - function ID: 00000009
        - description: Updates the value of a given gyroscope register
    """
    def resp_updateGyroRegister(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000009):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
        responseInstance["e__HwResult__status"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: readMagnetorquerData
        - function ID: 0000000A
        - description: Reads the status of a given magnetorquer
    """
    def req_readMagnetorquerData(self, e__PanelId__id):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x0000000A
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_PanelId(e__PanelId__id).serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x0000000A, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: readMagnetorquerData
        - function ID: 0000000A
        - description: Reads the status of a given magnetorquer
    """
    def resp_readMagnetorquerData(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x0000000A):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_MagnetorquerInfo.deserialize(data, currentPos)
        responseInstance["s__regData"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: applyMagnetorquerData
        - function ID: 0000000B
        - description: Updates the operating parameters of a given magnetorquer
    """
    def req_applyMagnetorquerData(self, e__PanelId__id, uint8__powerPerc, uint8__direction):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x0000000B
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_PanelId(e__PanelId__id).serialize()
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__powerPerc)
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__direction)
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x0000000B, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: applyMagnetorquerData
        - function ID: 0000000B
        - description: Updates the operating parameters of a given magnetorquer
    """
    def resp_applyMagnetorquerData(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x0000000B):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
        responseInstance["e__HwResult__status"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: readTemperatureData
        - function ID: 0000000C
        - description: Reads the temperature sensor measurements for all panels
    """
    def req_readTemperatureData(self):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x0000000C
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x0000000C, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: readTemperatureData
        - function ID: 0000000C
        - description: Reads the temperature sensor measurements for all panels
    """
    def resp_readTemperatureData(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x0000000C):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_TemperatureInfo.deserialize(data, currentPos)
        responseInstance["s__tempData"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: getPhotometricInfo
        - function ID: 0000000D
        - description: Provides the ADC photosensor readings for all six panels
    """
    def req_getPhotometricInfo(self):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x0000000D
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x0000000D, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: getPhotometricInfo
        - function ID: 0000000D
        - description: Provides the ADC photosensor readings for all six panels
    """
    def resp_getPhotometricInfo(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x0000000D):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_PanelPhotometricInfo.deserialize(data, currentPos)
        responseInstance["s__data"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: getGpOutputStates
        - function ID: 0000000E
        - description: Provides the states of all OBC general-purpose outputs
    """
    def req_getGpOutputStates(self):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x0000000E
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x0000000E, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: getGpOutputStates
        - function ID: 0000000E
        - description: Provides the states of all OBC general-purpose outputs
    """
    def resp_getGpOutputStates(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x0000000E):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_GpioStatus.deserialize(data, currentPos)
        responseInstance["s__data"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: setGpOutputState
        - function ID: 0000000F
        - description: Triggers a change in the specified output pin state
    """
    def req_setGpOutputState(self, uint8__pinId, bool__value):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x0000000F
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", uint8__pinId)
        requestBytes += SerDesHelpers.serdesType_basic.serialize("uint8", bool__value)
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x0000000F, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: setGpOutputState
        - function ID: 0000000F
        - description: Triggers a change in the specified output pin state
    """
    def resp_setGpOutputState(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x0000000F):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.enum_HwResult.deserialize(data, currentPos)
        responseInstance["e__HwResult__opResult"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: getSensorsInUse
        - function ID: 00000010
        - description: Obtains information on the number of active users for a given OBC sensor
    """
    def req_getSensorsInUse(self, e__ObcSensor__sensor):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000010
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_ObcSensor(e__ObcSensor__sensor).serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000010, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: getSensorsInUse
        - function ID: 00000010
        - description: Obtains information on the number of active users for a given OBC sensor
    """
    def resp_getSensorsInUse(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000010):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_SensorInUseData.deserialize(data, currentPos)
        responseInstance["s__opResult"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: triggerSensorCommand
        - function ID: 00000011
        - description: Triggers the execution of a sensor command. Some of the sensor operations require sensor reservation command to be set first so that
                              power to the sensor is supplied.
    """
    def req_triggerSensorCommand(self, e__ObcSensor__sensor, e__ObcSensorCmd__cmdId):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000011
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_ObcSensor(e__ObcSensor__sensor).serialize()
        requestBytes += FP_API_OBC.enum_ObcSensorCmd(e__ObcSensorCmd__cmdId).serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000011, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: triggerSensorCommand
        - function ID: 00000011
        - description: Triggers the execution of a sensor command. Some of the sensor operations require sensor reservation command to be set first so that
                              power to the sensor is supplied.
    """
    def resp_triggerSensorCommand(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000011):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_SensorInUseData.deserialize(data, currentPos)
        responseInstance["s__opResult"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: getI2CPullUpsState
        - function ID: 00000012
        - description: Obtains information on state of the I2C Pull-Up resistors for system and
                              customer payload buses
    """
    def req_getI2CPullUpsState(self):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000012
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000012, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: getI2CPullUpsState
        - function ID: 00000012
        - description: Obtains information on state of the I2C Pull-Up resistors for system and
                              customer payload buses
    """
    def resp_getI2CPullUpsState(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000012):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_I2CPullUpsState.deserialize(data, currentPos)
        responseInstance["s__nvm_pullupsState"] = field
        currentPos += bytesProcessed
    
        field, bytesProcessed = FP_API_OBC.struct_I2CPullUpsState.deserialize(data, currentPos)
        responseInstance["s__io_pullupsState"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: setI2CPullUpsState
        - function ID: 00000013
        - description: Reconfigures the state of the I2C Pull-Up resistors for system and
                              customer payload buses
    """
    def req_setI2CPullUpsState(self, s__pullupsState):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000013
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += s__pullupsState.serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000013, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: setI2CPullUpsState
        - function ID: 00000013
        - description: Reconfigures the state of the I2C Pull-Up resistors for system and
                              customer payload buses
    """
    def resp_setI2CPullUpsState(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000013):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_I2CPullUpsState.deserialize(data, currentPos)
        responseInstance["s__pullupsIoState"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: getUptime
        - function ID: 00000018
        - description: Obtains the up time of the OBC since last power on.
    """
    def req_getUptime(self):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000018
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000018, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: getUptime
        - function ID: 00000018
        - description: Obtains the up time of the OBC since last power on.
    """
    def resp_getUptime(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000018):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_UptimeInfo.deserialize(data, currentPos)
        responseInstance["s__upTime"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: getResetCounters
        - function ID: 0000002A
        - description: Obtains the current values of the MCU reset counters
    """
    def req_getResetCounters(self):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x0000002A
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x0000002A, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: getResetCounters
        - function ID: 0000002A
        - description: Obtains the current values of the MCU reset counters
    """
    def resp_getResetCounters(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x0000002A):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.struct_ResetCountersInfo.deserialize(data, currentPos)
        responseInstance["s__status"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: clearResetCounter
        - function ID: 0000002B
        - description: Clears a given MCU reset counter
    """
    def req_clearResetCounter(self, e__ResetCntrId__id):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x0000002B
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_ResetCntrId(e__ResetCntrId__id).serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x0000002B, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: clearResetCounter
        - function ID: 0000002B
        - description: Clears a given MCU reset counter
    """
    def resp_clearResetCounter(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x0000002B):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.enum_StandardResult.deserialize(data, currentPos)
        responseInstance["e__StandardResult__opResult"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: triggerResetInMode
        - function ID: 00000036
        - description: Triggers a reset of the OBC starting with the specified APP mode
    """
    def req_triggerResetInMode(self, e__ApplicationMode__startMode):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x00000036
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        requestBytes += FP_API_OBC.enum_ApplicationMode(e__ApplicationMode__startMode).serialize()
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x00000036, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: triggerResetInMode
        - function ID: 00000036
        - description: Triggers a reset of the OBC starting with the specified APP mode
    """
    def resp_triggerResetInMode(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x00000036):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.enum_StandardResult.deserialize(data, currentPos)
        responseInstance["e__StandardResult__opResult"] = field
        currentPos += bytesProcessed
    
        return responseInstance

    ############################################################################################################
    """
    Request function for FIDL method: triggerFwUpdate
        - function ID: 0000003F
        - description: Triggers an OBC firmware Update from a user-defined file (the operation is performed after reseting to bootloader mode via the triggerResetInMode() operation)
    """
    def req_triggerFwUpdate(self, a__uint8__15__fileName):
        requestBytes = bytearray()
    
        if not self.rawSerDesSupport:
            fpHeaderInstance = SerDesHelpers.struct_FPHeader()
    
            fpHeaderInstance.u16ProtoId = self.const_OBC_PROTOCOL_ID
            fpHeaderInstance.u32FuncId = 0x0000003F
            fpHeaderInstance.u16seqId = 0
            fpHeaderInstance.u8ErrCode = 0
    
            requestBytes += fpHeaderInstance.serialize()
    
        actualLen = len(a__uint8__15__fileName)
    
        if (actualLen > 15):
            raise Exception("The maximum expected size for array argument a__uint8__15__fileName is 15 bytes but " + str(actualLen) + " bytes were provided.")
        requestBytes += SerDesHelpers.serdesType_basicArray.serialize("uint8", a__uint8__15__fileName, 15)
    
        if not self.rawSerDesSupport:
            return requestBytes
        else:
            return (0x0000003F, requestBytes)

    ############################################################################################################
    """
    Response function for FIDL method: triggerFwUpdate
        - function ID: 0000003F
        - description: Triggers an OBC firmware Update from a user-defined file (the operation is performed after reseting to bootloader mode via the triggerResetInMode() operation)
    """
    def resp_triggerFwUpdate(self, data):
        # (key, value) = (output arg name, output arg data)
        responseInstance = {}
    
        if not self.rawSerDesSupport:
            fpHeaderInstance, headerBytesProcessed = SerDesHelpers.struct_FPHeader.deserialize(data, 0)
    
            if (fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID) or (fpHeaderInstance.u32FuncId != 0x0000003F):
               raise Exception("Protocol ID and/or Function ID do not match to the called response method!")
    
            currentPos = headerBytesProcessed
        else:
            currentPos = 0
    
    
        field, bytesProcessed = FP_API_OBC.enum_StandardResult.deserialize(data, currentPos)
        responseInstance["e__StandardResult__opResult"] = field
        currentPos += bytesProcessed
    
        return responseInstance


    ############################################################################################################
    """
    Deserializes the provided bytearray and returns a dictionary of parsed values for the response;
    functionId parameter shall be supplied if the class is used in rawSerDesSupport mode, otherwise
    it is extracted from the FP header
    """
    def resp_parse(self, respBytes, functionId : int = 0):
        if not self.rawSerDesSupport:
            # try to parse FunctionProtocol header
            (fpHeaderInstance, bytesProcessed) = SerDesHelpers.struct_FPHeader.deserialize(respBytes, 0)
            funcId = fpHeaderInstance.u32FuncId

            if fpHeaderInstance.u16ProtoId != self.const_OBC_PROTOCOL_ID:
                raise Exception("Unsupported protocol ID", fpHeaderInstance.u16ProtoId)
        else:
            funcId = functionId

        if funcId in self.responseParsersDict:
            respParserFunc = self.responseParsersDict[funcId]
            return respParserFunc(respBytes) if respParserFunc is not None else None
        else:
            raise Exception('Unsupported function id', hex(funcId))
    ############################################################################################################
    """
    Returns the Protocol version as a string vM.m
    """
    def get_version(self):
        return f'v{self.versionMajor}.{self.versionMinor}'
    ############################################################################################################

