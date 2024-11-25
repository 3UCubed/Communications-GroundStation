 ##############################################################################
 # @file           : realtime_beacon_parser.py
 # @author 		   : Jared Morrison
 # @date	 	   : November 18, 2024
 # @brief          : Parses beacons in real time and prints output to console.
 ##############################################################################


import subprocess
import os
from struct import unpack_from
from itertools import islice


# @brief Executes a command and yields its output line by line.
# 
# @details This function runs a command using subprocess.Popen and returns the standard output of the command
#          line by line. It handles a keyboard interrupt by terminating the process and closing the output stream.
# 
# @param cmd The command to execute, provided as a list of strings.
# @yield The output from the command, line by line.

def execute(cmd):
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    try:
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
    except KeyboardInterrupt:
        print("Keyboard interrupt...")
        popen.terminate()
        popen.wait()
        popen.stdout.close()
        popen.wait()


# @brief Represents the header of a beacon message.
# 
# @details Private class used by BeaconMsg to parse out a message header

class BeaconMsgHeader:
    MSG_HEADER_SIZE = 4

    # Used for translating the dc_id hex value to the actual DC attribute name
    dc_entries_dict = {
        0x00000010: "OBC_0",
        0x00000011: "ADCS_0",
        0x00000012: "ADCS_1",
        0x00000013: "ADCS_2",
        0x00000014: "EPS_0",
        0x00000015: "SSP_0",
        0x00000016: "SSP_1",
        0x00000017: "SSP_2",
        0x00000019: "AOCS_CNTRL_TLM",
        0x0000001A: "EPS_1",
        0x0000001B: "EPS_2",
        0x0000001C: "EPS_3",
        0x0000001D: "EPS_4",
        0x0000001E: "EPS_5",
        0x0000001F: "EPS_6",
        0x00000020: "TaskStats",
        0x00000021: "SSP_3",
        0x00000022: "SENSOR_MAG_PRIMARY",
        0x00000023: "SENSOR_MAG_SECONDARY",
        0x00000024: "SENSOR_GYRO",
        0x00000025: "SENSOR_COARSE_SUN",
        0x00000026: "ES_ADCS_SENSOR_MAG_PRIMARY",
        0x00000027: "ES_ADCS_SENSOR_MAG_SECONDARY",
        0x00000028: "ES_ADCS_SENSOR_GYRO",
        0x00000029: "ES_ADCS_SENSOR_CSS",
        0x00000030: "ES_ADCS_ESTIMATES_BDOT",
        0x00000031: "ES_ADCS_CONTROL_VALUES_MTQ",
        0x00000032: "ConOpsFlags",
        0x00000033: "AOCS_CNTRL_SYS_STATE",
        0x00000034: "ADCS_3",
        0x00000035: "ADCS_4",
        0x000000FF: "Unknown"
    }
    
    def __init__(self):
        self.dc_id = 0
        self.flag_d = 0
        self.flag_e = 0
        self.msg_length = 0
    
    def parse(self, data: bytes):
        if len(data) >= BeaconMsgHeader.MSG_HEADER_SIZE:
            (
                self.dc_id,
                self.flag_d,
                self.flag_e,
                self.msg_length
            ) = unpack_from("<BBBB", data)
            self.dc_id = BeaconMsgHeader.dc_entries_dict[self.dc_id]
            return BeaconMsgHeader.MSG_HEADER_SIZE
        else:
            return 0


# @brief Represents a beacon message.
# 
# @details Private class used by the Beacon class. For each message within a beacon,
#          the Beacon class creates a new instance of BeaconMsg.

class BeaconMsg:
    def __init__(self):
        self.header = BeaconMsgHeader()
        self.data = []
        self.labeled_data = {}
        self.partial = False

    def parse(self, data: bytes):
            
        for byte in data:
            self.data.append(byte)
        
    def label(self):
        if self.header.dc_id == "OBC_0":
            self.labeled_data = BeaconMsg.parse_obc_0(self.data)
        elif self.header.dc_id == "ADCS_0":
            self.labeled_data = BeaconMsg.parse_adcs_0(self.data)
        elif self.header.dc_id == "ADCS_1":
            self.labeled_data = BeaconMsg.parse_adcs_1(self.data)
        elif self.header.dc_id == "ADCS_2":
            self.labeled_data = BeaconMsg.parse_adcs_2(self.data)
        elif self.header.dc_id == "EPS_0":
            self.labeled_data = BeaconMsg.parse_eps_0(self.data)
        elif self.header.dc_id == "SSP_0" or self.header.dc_id == "SSP_1" or self.header.dc_id == "SSP_2" or self.header.dc_id == "SSP_3":
            self.labeled_data = BeaconMsg.parse_ssp(self.data)
        elif self.header.dc_id == "AOCS_CNTRL_TLM":
            self.labeled_data = BeaconMsg.parse_aocs_cntrl_tlm(self.data)
        elif self.header.dc_id == "EPS_1":
            self.labeled_data = BeaconMsg.parse_eps_1(self.data)
        elif self.header.dc_id == "EPS_2":
            self.labeled_data = BeaconMsg.parse_eps_2(self.data)
        elif self.header.dc_id == "EPS_3":
            self.labeled_data = BeaconMsg.parse_eps_3(self.data)
        elif self.header.dc_id == "EPS_4":
            self.labeled_data = BeaconMsg.parse_eps_4(self.data)
        elif self.header.dc_id == "EPS_5":
            self.labeled_data = BeaconMsg.parse_eps_5(self.data)
        elif self.header.dc_id == "EPS_6":
            self.labeled_data = BeaconMsg.parse_eps_6(self.data)
        elif self.header.dc_id == "TaskStats":
            self.labeled_data = BeaconMsg.parse_taskstats(self.data)
        elif self.header.dc_id == "SENSOR_MAG_PRIMARY" or self.header.dc_id == 'SENSOR_MAG_SECONDARY':
            self.labeled_data = BeaconMsg.parse_sensor_mag(self.data)
        elif self.header.dc_id == "SENSOR_GYRO":
            self.labeled_data = BeaconMsg.parse_sensor_gyro(self.data)
        elif self.header.dc_id == "SENSOR_COARSE_SUN":
            self.labeled_data = BeaconMsg.parse_sensor_coarse_sun(self.data)
        elif self.header.dc_id == "ES_ADCS_SENSOR_MAG_PRIMARY" or self.header.dc_id == "ES_ADCS_SENSOR_MAG_SECONDARY":
            self.labeled_data = BeaconMsg.parse_es_adcs_sensor_mag(self.data)
        elif self.header.dc_id == "ES_ADCS_SENSOR_GYRO":
            self.labeled_data = BeaconMsg.parse_es_adcs_sensor_gyro(self.data)
        elif self.header.dc_id == "ES_ADCS_SENSOR_CSS":
            self.labeled_data = BeaconMsg.parse_es_adcs_sensor_css(self.data)
        elif self.header.dc_id == "ES_ADCS_ESTIMATES_BDOT":
            self.labeled_data = BeaconMsg.parse_es_adcs_estimates_bdot(self.data)
        elif self.header.dc_id == "ES_ADCS_CONTROL_VALUES_MTQ":
            self.labeled_data = BeaconMsg.parse_es_adcs_control_values_mtq(self.data)
        elif self.header.dc_id == "ConOpsFlags":
            self.labeled_data = BeaconMsg.parse_conops_flags(self.data)
        elif self.header.dc_id == "AOCS_CNTRL_SYS_STATE":
            self.labeled_data = BeaconMsg.parse_aocs_cntrl_sys_state(self.data)
        elif self.header.dc_id == "ADCS_3":
            self.labeled_data = BeaconMsg.parse_adcs_3(self.data)
        elif self.header.dc_id == "ADCS_4":
            self.labeled_data = BeaconMsg.parse_adcs_4(self.data)
        else:
            self.labeled_data = BeaconMsg.parse_other(self.data)
    
    @staticmethod
    def parse_other(data: bytes):
        labeled_data = {}
        for key, value in enumerate(data):
            labeled_data[f"{key}"] = value
        return labeled_data

    @staticmethod
    def parse_obc_0(data: bytes):
        labeled_data = {}

        labeled_data['opMode'] = data[0]
        labeled_data['upTime'] = int.from_bytes(data[1:5], byteorder='little', signed=False)
        labeled_data['totalResetCount'] = int.from_bytes(data[5:7], byteorder='little', signed=False)
        labeled_data['resetReasonBitField'] = int.from_bytes(data[7:9], byteorder='little', signed=False)
        labeled_data['payloadModesStatus'] = int.from_bytes(data[9:11], byteorder='little', signed=False)

        return labeled_data

    @staticmethod
    def parse_adcs_0(data: bytes):
        labeled_data = {}
        shifted_data = []
        data_keys = [
            'magFieldVec_X', 'magFieldVec_Y', 'magFieldVec_Z',
            'coarseSunVec_X', 'coarseSunVec_Y', 'coarseSunVec_Z',
            'fineSunVec_X', 'fineSunVec_Y', 'fineSunVec_Z',
            'nadirVec_X', 'nadirVec_Y', 'nadirVec_Z',
            'angRateVec_X', 'angRateVec_Y', 'angRateVec_Z',
            'wheelSpeedArr_X', 'wheelSpeedArr_Y', 'wheelSpeedArr_Z'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for key, value in zip(data_keys, shifted_data):
            labeled_data[key] = value
        
        return labeled_data
    
    @staticmethod
    def parse_adcs_1(data: bytes):
        labeled_data = {}
        shifted_data = []
        data_keys = [
            'estQSet_Q1', 'estQSet_Q2', 'estQSet_Q3',
            'estQSet_X', 'estQSet_Y', 'estQSet_Z'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for key, value in zip(data_keys, shifted_data):
            labeled_data[key] = value
        
        return labeled_data
    
    @staticmethod
    def parse_adcs_2(data: bytes):
        labeled_data = {}
        byte_0 = data[0]
        byte_1 = data[1]
        byte_2 = data[2]
        byte_3 = data[3]
        byte_4 = data[4]
        byte_5 = data[5]

        labeled_data['Attitude_Estimation_Mode'] = byte_0 & 0b1111  
        labeled_data['Control_Mode'] = (byte_0 >> 4) & 0b1111           
        
        labeled_data['ADCS_Run_Mode'] = byte_1 & 0b1                      
        labeled_data['ASGP4_Mode'] = (byte_1 >> 1) & 0b1                   
        labeled_data['CubeControl_Signal_Enabled'] = (byte_1 >> 2) & 0b1    
        labeled_data['CubeControl_Motor_Enabled'] = (byte_1 >> 3) & 0b1    
        labeled_data['CubeSense1_Enabled'] = (byte_1 >> 4) & 0b11       
        labeled_data['CubeSense2_Enabled'] = (byte_1 >> 6) & 0b11         

        labeled_data['CubeWheel1_Enabled'] = byte_2 & 0b1                  
        labeled_data['CubeWheel2_Enabled'] = (byte_2 >> 1) & 0b1           
        labeled_data['CubeWheel3_Enabled'] = (byte_2 >> 2) & 0b1           
        labeled_data['CubeStar_Enabled'] = (byte_2 >> 3) & 0b1            
        labeled_data['GPS_Receiver_Enabled'] = (byte_2 >> 4) & 0b1          
        labeled_data['GPS_LNA_Power_Enabled'] = (byte_2 >> 5) & 0b1         
        labeled_data['Motor_Driver_Enabled'] = (byte_2 >> 6) & 0b1          
        labeled_data['Sun_is_Above_Local_Horizon'] = (byte_2 >> 7) & 0b1    

        labeled_data['CubeSense1_Communications_Error'] = byte_3 & 0b1                 
        labeled_data['CubeSense2_Communications_Error'] = (byte_3 >> 1) & 0b1       
        labeled_data['CubeControl_Signal_Communications_Error'] = (byte_3 >> 2) & 0b1  
        labeled_data['CubeControl_Motor_Communications_Error'] = (byte_3 >> 3) & 0b1    
        labeled_data['CubeWheel1_Communications_Error'] = (byte_3 >> 4) & 0b1          
        labeled_data['CubeWheel2_Communications_Error'] = (byte_3 >> 5) & 0b1        
        labeled_data['CubeWheel3_Communications_Error'] = (byte_3 >> 6) & 0b1        
        labeled_data['CubeStar_Communications_Error'] = (byte_3 >> 7) & 0b1            

        labeled_data['Magnetometer_Range_Error'] = byte_4 & 0b1                 
        labeled_data['Cam1_SRAM_Overcurrent_Detected'] = (byte_4 >> 1) & 0b1    
        labeled_data['Cam1_3V3_Overcurrent_Detected'] = (byte_4 >> 2) & 0b1     
        labeled_data['Cam1_Sensor_Busy_Error'] = (byte_4 >> 3) & 0b1          
        labeled_data['Cam1_Sensor_Detection_Error'] = (byte_4 >> 4) & 0b1     
        labeled_data['Sun_Sensor_Range_Error'] = (byte_4 >> 5) & 0b1           
        labeled_data['Cam2_SRAM_Overcurrent_Detected'] = (byte_4 >> 6) & 0b1   
        labeled_data['Cam2_3V3_Overcurrent_Detected'] = (byte_4 >> 7) & 0b1     

        labeled_data['Cam2_Sensor_Busy_Error'] = byte_5 & 0b1                   
        labeled_data['Cam2_Sensor_Detection_Error'] = (byte_5 >> 1) & 0b1       
        labeled_data['Nadir_Sensor_Range_Error'] = (byte_5 >> 2) & 0b1          
        labeled_data['Rate_Sensor_Range_Error'] = (byte_5 >> 3) & 0b1           
        labeled_data['Wheel_Speed_Range_Error'] = (byte_5 >> 4) & 0b1           
        labeled_data['Coarse_Sun_Sensor_Error'] = (byte_5 >> 5) & 0b1           
        labeled_data['StarTracker_Match_Error'] = (byte_5 >> 6) & 0b1           
        labeled_data['StarTracker_Overcurrent_Detected'] = (byte_5 >> 7) & 0b1  

        return labeled_data

    @staticmethod
    def parse_eps_0(data: bytes):
        labeled_data = {}

        labeled_data['battEnergy'] = int.from_bytes(data[0:8], byteorder='little', signed=True)
        labeled_data['battCharge'] = int.from_bytes(data[8:16], byteorder='little', signed=True)
        labeled_data['battChargeCapacity'] = int.from_bytes(data[16:24], byteorder='little', signed=True)
        labeled_data['battPercent'] = int.from_bytes(data[24:32], byteorder='little', signed=True)
        labeled_data['battVoltage'] = int.from_bytes(data[32:36], byteorder='little', signed=True)
        labeled_data['battCurrent'] = int.from_bytes(data[36:40], byteorder='little', signed=True)
        labeled_data['battTemperature'] = int.from_bytes(data[40:44], byteorder='little', signed=True)

        return labeled_data

    @staticmethod
    def parse_ssp(data: bytes):
        # All SSP's can be parsed exactly the same way
        labeled_data = {}
        shifted_data = []
        new_labels = ['sunDataMain', 'sunDataExt', 'tempMCU', 'tempMain', 'tempExt1', 'temptExt2']

        for i in range(0, 4, 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=False))
        
        for i in range(4, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value
        
        return labeled_data
    
    @staticmethod
    def parse_aocs_cntrl_tlm(data: bytes):
        labeled_data = {}

        labeled_data['adcsErrFlags'] = int.from_bytes(data[0:2], byteorder='little', signed=False)
        labeled_data['estAngRateNorm'] = int.from_bytes(data[2:6], byteorder='little', signed=True)
        labeled_data['estAngRateVec_X'] = int.from_bytes(data[6:10], byteorder='little', signed=True)
        labeled_data['estAngRateVec_Y'] = int.from_bytes(data[10:14], byteorder='little', signed=True)
        labeled_data['estAngRateVec_Z'] = int.from_bytes(data[14:18], byteorder='little', signed=True)
        labeled_data['estAttAngles_Roll'] = int.from_bytes(data[18:22], byteorder='little', signed=True)
        labeled_data['estAttAngles_Pitch'] = int.from_bytes(data[22:26], byteorder='little', signed=True)
        labeled_data['estAttAngles_Yaw'] = int.from_bytes(data[26:30], byteorder='little', signed=True)
        labeled_data['measWheelSpeed_X'] = int.from_bytes(data[30:32], byteorder='little', signed=True)
        labeled_data['measWheelSpeed_Y'] = int.from_bytes(data[32:34], byteorder='little', signed=True)
        labeled_data['measWheelSpeed_Z'] = int.from_bytes(data[34:36], byteorder='little', signed=True)

        return labeled_data
    
    @staticmethod
    def parse_eps_1(data: bytes):
        labeled_data = {}

        labeled_data['battCapacity'] = int.from_bytes(data[0:4], byteorder='little', signed=True)
        labeled_data['battVoltage'] = int.from_bytes(data[4:8], byteorder='little', signed=True)
        labeled_data['battCurrent'] = int.from_bytes(data[8:12], byteorder='little', signed=True)
        labeled_data['battTemperature'] = int.from_bytes(data[12:16], byteorder='little', signed=True)

        return labeled_data
    
    @staticmethod
    def parse_eps_2(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'VOLT_BRDSUP',
            'TEMP_MCU',
            'VIP_INPUT_Voltage',
            'VIP_INPUT_Current',
            'VIP_INPUT_Power',
            'STAT_CH_ON',
            'STAT_CH_OCF',
            'VIP_Voltage_VD0',
            'VIP_Current_VD0',
            'VIP_Voltage_VD4',
            'VIP_Current_VD4',
            'VIP_Voltage_VD6',
            'VIP_Current_VD6',
            'VIP_Voltage_VD7',
            'VIP_Current_VD7',
            'VIP_Voltage_VD8',
            'VIP_Current_VD8',
            'VIP_Voltage_VD9',
            'VIP_Current_VD9',
            'VIP_Voltage_VD10',
            'VIP_Current_VD10',
            'VIP_Voltage_VD11',
            'VIP_Current_VD11'
        ]

        for i in range(0, 10, 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for i in range(10, 14, 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=False))

        for i in range(14, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value
        
        return labeled_data
    
    @staticmethod
    def parse_eps_3(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'VOLT_BRDSUP',
            'TEMP_MCU',
            'VIP_INPUT_Voltage',
            'VIP_INPUT_Current',
            'VIP_INPUT_Power',
            'STAT_BU',
            'VIP_BP_INPUT_Voltage_1',
            'VIP_BP_INPUT_Voltage_2',
            'VIP_BP_INPUT_Current_1',
            'VIP_BP_INPUT_Current_2',
            'VIP_BP_INPUT_Power_1',
            'VIP_BP_INPUT_Power_2',
            'STAT_BP_1',
            'STAT_BP_2',
            'VOLT_CELL1_1',
            'VOLT_CELL1_2',
            'VOLT_CELL2_1',
            'VOLT_CELL2_2',
            'VOLT_CELL3_1',
            'VOLT_CELL3_2',
            'VOLT_CELL4_1',
            'VOLT_CELL4_2',
            'BAT_TEMP1_1',
            'BAT_TEMP1_2',
            'BAT_TEMP2_1',
            'BAT_TEMP2_2',
            'BAT_TEMP3_1',
            'BAT_TEMP3_2',
        ]

        for i in range(0, 10, 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))
        
        shifted_data.append(int.from_bytes(data[10:12], byteorder='little', signed=False))

        for i in range(12, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data
    
    @staticmethod
    def parse_eps_4(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'VOLT_BRDSUP',
            'TEMP_MCU',
            'VIP_OUTPUT_Voltage',
            'VIP_OUTPUT_Current',
            'VIP_OUTPUT_Power',
            'VIP_CC_OUTPUT_Voltage_1',
            'VIP_CC_OUTPUT_Voltage_2',
            'VIP_CC_OUTPUT_Voltage_3',
            'VIP_CC_OUTPUT_Voltage_4',
            'VIP_CC_OUTPUT_Current_1',
            'VIP_CC_OUTPUT_Current_2',
            'VIP_CC_OUTPUT_Current_3',
            'VIP_CC_OUTPUT_Current_4',
            'VIP_CC_OUTPUT_Power_1',
            'VIP_CC_OUTPUT_Power_2',
            'VIP_CC_OUTPUT_Power_3',
            'VIP_CC_OUTPUT_Power_4',
            'CCx_VOLT_IN_MPPT_1',
            'CCx_VOLT_IN_MPPT_2',
            'CCx_VOLT_IN_MPPT_3',
            'CCx_VOLT_IN_MPPT_4',
            'CCx_CURR_IN_MPPT_1',
            'CCx_CURR_IN_MPPT_2',
            'CCx_CURR_IN_MPPT_3',
            'CCx_CURR_IN_MPPT_4',
            'CCx_VOLT_OU_MPPT_1',
            'CCx_VOLT_OU_MPPT_2',
            'CCx_VOLT_OU_MPPT_3',
            'CCx_VOLT_OU_MPPT_4',
            'CCx_CURR_OU_MPPT_1',
            'CCx_CURR_OU_MPPT_2',
            'CCx_CURR_OU_MPPT_3',
            'CCx_CURR_OU_MPPT_4'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data

    @staticmethod
    def parse_eps_5(data: bytes):
        labeled_data = {}

        labeled_data['MODE'] = data[0]
        labeled_data['RESET_CAUSE'] = data[1]
        labeled_data['UPTIME'] = int.from_bytes(data[2:6], byteorder='little', signed=False)
        labeled_data['ERROR'] = int.from_bytes(data[6:8], byteorder='little', signed=False)
        labeled_data['RC_CNT_PWRON'] = int.from_bytes(data[8:10], byteorder='little', signed=False)
        labeled_data['RC_CNT_WDG'] = int.from_bytes(data[10:12], byteorder='little', signed=False)
        labeled_data['RC_CNT_CMD'] = int.from_bytes(data[12:14], byteorder='little', signed=False)
        labeled_data['RC_CNT_MCU'] = int.from_bytes(data[14:16], byteorder='little', signed=False)
        labeled_data['RC_CNT_EMLOPO'] = int.from_bytes(data[16:18], byteorder='little', signed=False)
        labeled_data['UNIX_TIME'] = int.from_bytes(data[18:22], byteorder='little', signed=False)
        labeled_data['UNIX_YEAR'] = int.from_bytes(data[22:26], byteorder='little', signed=False)
        labeled_data['UNIX_MONTH'] = int.from_bytes(data[26:30], byteorder='little', signed=False)
        labeled_data['UNIX_DAY'] = int.from_bytes(data[30:34], byteorder='little', signed=False)
        labeled_data['UNIX_HOUR'] = int.from_bytes(data[34:38], byteorder='little', signed=False)
        labeled_data['UNIX_MINUTE'] = int.from_bytes(data[38:42], byteorder='little', signed=False)
        labeled_data['UNIX_SECOND'] = int.from_bytes(data[42:46], byteorder='little', signed=False)

        return labeled_data
    
    @staticmethod
    def parse_eps_6(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'STAT_CH_ON',
            'STAT_CH_OCF',
            'OCF_CNT_CH00',
            'OCF_CNT_CH04',
            'OCF_CNT_CH06',
            'OCF_CNT_CH07',
            'OCF_CNT_CH08',
            'OCF_CNT_CH09',
            'OCF_CNT_CH10',
            'OCF_CNT_CH11'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=False))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data
    
    @staticmethod
    def parse_taskstats(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'TASK_MONITOR_TASK',
            'TASK_MONITOR_EXEH_PERSISTOR',
            'TASK_MONITOR_APP_TASK',
            'TASK_MONITOR_SERVICES',
            'TASK_MONITOR_SD_MANAGER',
            'TASK_INSTRUMENTS',
            'TASK_MONITOR_S_X_BAND',
            'TASK_MONITOR_CUBEADCS',
            'TASK_MONITOR_CUBEADCS_FHANDL',
            'TASK_MONITOR_GNSS',
            'TASK_PAYLOAD_SCHEDULER',
            'TASK_TELEMETRY',
            'TASK_TELEMETRY_FILE_SINK',
            'TASK_MONITOR_SP',
            'TASK_MACDRV_DISPATCHER',
            'TASK_MACTL_DISPATCHER',
            'TASK_FWUPD_HANDLER',
            'TASK_ESSA_SP_HANDLER',
            'TASK_NVM',
            'TASK_DATACACHE',
            'TASK_ADCS_TLM',
            'TASK_CONOPS_PERIODIC_EV',
            'TASK_MONITOR_PAYLOAD_CTRL',
            'TASK_BEACONS',
            'TASK_EPS_CTRL',
            'TASK_EPS_I',
            'TASK_EPS_II',
            'TASK_EPS_M',
            'TASK_SYS_CLOCK',
            'TASK_MONITOR_ES_ADCS',
            'TASK_ACTUATOR_CONTROL_SERVICE',
            'TASK_SDS',
            'TASK_AOCS_CNTRL',
            'TASK_SXBAND_SCHED',
            'TASK_CRYPTO_SRV',
            'TASK_MONITOR_TASKS_NUMBER'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for key, value in zip(islice(new_labels, len(shifted_data)), shifted_data):
            labeled_data[key] = value

        return labeled_data

    @staticmethod
    def parse_sensor_mag(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'int32__MAG_X',
            'int32__MAG_Y',
            'int32__MAG_Z'
        ]

        for i in range(0, len(data), 4):
            shifted_data.append(int.from_bytes(data[i:i+4], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data

    @staticmethod
    def parse_sensor_gyro(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'int32__GYRO_1',
            'int32__GYRO_2',
            'int32__GYRO_3'
        ]

        for i in range(0, len(data), 4):
            shifted_data.append(int.from_bytes(data[i:i+4], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data

    @staticmethod
    def parse_sensor_coarse_sun(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'CSS_PANEL_1',
            'CSS_PANEL_2',
            'CSS_PANEL_3',
            'CSS_PANEL_4',
            'CSS_PANEL_5',
            'CSS_PANEL_6'
        ]

        for i in range(0, len(data), 4):
            shifted_data.append(int.from_bytes(data[i:i+4], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data

    @staticmethod
    def parse_es_adcs_sensor_mag(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'MAG_X_CURRENT',
            'MAG_Y_CURRENT',
            'MAG_Z_CURRENT',
            'MAG_X_PREVIOUS',
            'MAG_Y_PREVIOUS',
            'MAG_Z_PREVIOUS'
        ]

        for i in range(0, len(data), 4):
            shifted_data.append(int.from_bytes(data[i:i+4], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data
    
    @staticmethod
    def parse_es_adcs_sensor_gyro(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'GYRO_X',
            'GYRO_Y',
            'GYRO_Z'
        ]

        for i in range(0, len(data), 4):
            shifted_data.append(int.from_bytes(data[i:i+4], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data
    
    @staticmethod
    def parse_es_adcs_sensor_css(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'CSS_AXIS_X_PLUS',
            'CSS_AXIS_Y_PLUS',
            'CSS_AXIS_Z_PLUS',
            'CSS_AXIS_X_MINUS',
            'CSS_AXIS_Y_MINUS',
            'CSS_AXIS_Z_MINUS'
        ]

        for i in range(0, len(data), 4):
            shifted_data.append(int.from_bytes(data[i:i+4], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data
    
    @staticmethod
    def parse_es_adcs_estimates_bdot(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'MAG_FIELD_DERIV_X',
            'MAG_FIELD_DERIV_Y',
            'MAG_FIELD_DERIV_Z'
        ]

        for i in range(0, len(data), 4):
            shifted_data.append(int.from_bytes(data[i:i+4], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data
    
    @staticmethod
    def parse_es_adcs_control_values_mtq(data: bytes):
        labeled_data = {}
        new_labels = [
            'MAGTORQUE_VALUE_X',
            'MAGTORQUE_VALUE_Y',
            'MAGTORQUE_VALUE_Z'
        ]

        for key, value in zip(new_labels, data):
            labeled_data[key] = int.from_bytes(value, byteorder='little', signed=True) 
        
        return labeled_data
    
    @staticmethod
    def parse_conops_flags(data: bytes):
        labeled_data = {}
        new_labels = [
            'PAY_ERR',
            'ADCS_ERR',
            'DETUMB_COMPLETED'
        ]

        for key, value in zip(new_labels, data):
            labeled_data[key] = int.from_bytes(value, byteorder='little', signed=False)  
        
        return labeled_data
    
    @staticmethod
    def parse_aocs_cntrl_sys_state(data: bytes):
        labeled_data = {}
        new_labels = [
            'adcsSysState',
            'adcsSysStateStatus',
        ]

        for key, value in zip(new_labels, data):
            labeled_data[key] = labeled_data[key] = int.from_bytes(value, byteorder='little', signed=False) 
        
        return labeled_data
    
    @staticmethod
    def parse_adcs_3(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'est_roll_angle',
            'est_pitch_angle',
            'est_yaw_angle',
            'IGRF_MagField_X',
            'IGRF_MagField_Y',
            'IGRF_MagField_Z',
            'Modelled_Sun_V_X',
            'Modelled_Sun_V_Y',
            'Modelled_Sun_V_Z',
            'EstGyroBias_X',
            'EstGyroBias_Y',
            'EstGyroBias_Z',
            'Innovation_Vec_X',
            'Innovation_Vec_Y',
            'Innovation_Vec_Z',
            'Err_Q1',
            'Err_Q2',
            'Err_Q3',
            'RMS_Q1',
            'RMS_Q2',
            'RMS_Q3',
            'X_AngRate_Cov',
            'Y_AngRate_Cov',
            'Z_AngRate_Cov',
            'X_Rate',
            'Y_Rate',
            'Z_Rate',
            'Q0',
            'Q1',
            'Q2'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data
    
    @staticmethod
    def parse_adcs_4(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'Cubesense1_3V3_Current'
            'Cubesense1_SRAM_Current'
            'Cubesense2_3V3_Current'
            'Cubesense2_SRAM_Current'
            'CubeControl_3V3_Current'
            'CubeControl_5V_Current'
            'CubeControl_Vbat_Current'
            'Wheel_1_Current'
            'Wheel_2_Current'
            'Wheel_3_Current'
            'CubeStar_Current'
            'MTQ_Current'
            'CubeStar_MCU_Temp'
            'ADCS_MCU_Temp'
            'MTM_Temp'
            'RMTM_Temp'
            'X_Rate_Sensor_Temp'
            'Y_Rate_Sensor_Temp'
            'Z_Rate_Sensor_Temp'
        ]

        for i in range(0, 24, 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=False))

        for i in range(24, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data

    def __str__(self):
        str_repr = f"\nBeaconMsgHeader> DC ID: {self.header.dc_id} | Flag D: {hex(self.header.flag_d)} | Flag E: {hex(self.header.flag_e)} | MSG Length: {hex(self.header.msg_length)}\n"
        str_repr += "BeaconMsgData>\n" + "\n".join(f"{str(key) + ':':<40} {value}" for key, value in self.labeled_data.items())
        return str_repr


# @brief Represents the structure of a beacon header.
#
# @details Private class used by the Beacon class to parse beacon headers.
#          For each beacon, a new instance of BeaconHeader is created.

class BeaconHeader:
    HEADER_SIZE = 7
   
    def __init__(self):
        self.beacon_consecutive_number = 0
        self.uhf_address = 0
        self.flag_a = 0
        self.obc_address = 0
        self.data_id = 0
        self.flag_b = 0
        self.flag_c = 0
    
    def parse(self, data: bytes):
        if len(data) >= BeaconHeader.HEADER_SIZE:
            (
                self.beacon_consecutive_number,
                self.uhf_address,
                self.flag_a,
                self.obc_address,
                self.data_id,
                self.flag_b,
                self.flag_c
            ) = unpack_from("<BBBBBBB", data)
            return BeaconHeader.HEADER_SIZE
        else:
            return 0
    
    def __str__(self):
        return f"\n\nBeaconHeader> Beacon Consecutive Number: {hex(self.beacon_consecutive_number)} | UHF Address: {hex(self.uhf_address)} | Flag A: {hex(self.flag_a)} | OBC Address: {hex(self.obc_address)} | Data ID: {hex(self.data_id)} | Flag B: {hex(self.flag_b)} | Flag C: {hex(self.flag_c)}"


# @brief Represents the structure of an entire beacon.
#
# @details Public class used to parse beacons. Each output line of the
#          spacecomms interface script corresponds to a new beacon. So,
#          for each output line received from the spacecomms script, a
#          new instance of this class is created. 

class Beacon:
    BEACON_SIZE = 77
    def __init__(self, data: bytes):
        self.beacon_header = BeaconHeader()
        self.msg_list = []
        self.data = data
        self.current_pos = 0

    def parse(self):
        header_data = self.data[:BeaconHeader.HEADER_SIZE]
        self.beacon_header.parse(header_data)
        self.current_pos = BeaconHeader.HEADER_SIZE

        while self.current_pos < Beacon.BEACON_SIZE - BeaconMsgHeader.MSG_HEADER_SIZE:
            msg = BeaconMsg()
            msg_header_data = self.data[self.current_pos:self.current_pos + BeaconMsgHeader.MSG_HEADER_SIZE]
            msg.header.parse(msg_header_data)
            self.current_pos += BeaconMsgHeader.MSG_HEADER_SIZE

            if msg.header.dc_id == 'Unknown':
                break

            if self.current_pos + msg.header.msg_length > Beacon.BEACON_SIZE:
                msg_data = self.data[self.current_pos:Beacon.BEACON_SIZE]
                msg.parse(msg_data)
                msg.partial = True
            else:
                msg_data = self.data[self.current_pos:self.current_pos + msg.header.msg_length]
                msg.parse(msg_data)

            self.current_pos += msg.header.msg_length
            
            self.msg_list.append(msg)  


# @brief Main function to listen for and process beacon messages.
# 
# @details This script listens for beacon messages from the spacecomms interface, parses the received data, 
#          and organizes it into complete messages. If a partial message is detected, it waits for the remaining 
#          data to complete the message. The complete messages are labeled and added to the message list, and each
#          complete message is printed.

def parse(raw_beacon_queue, parsed_beacon_queue, parsing_beacons):
    cmplt_msg_list = []
    partial_msg = None
    complete_msg = None

    while parsing_beacons.is_set():

        if not raw_beacon_queue.empty():
            byte_data = raw_beacon_queue.get()
        else:
            continue

        # Create and parse new beacon
        new_beacon = Beacon(byte_data)
        new_beacon.parse()
        
        # Check if the previous message was partial
        if partial_msg is not None:
            # If so, set complete message to partial message and add the data of the new message
            complete_msg = partial_msg
            complete_msg.data += new_beacon.msg_list[0].data

            # Add the newly completed message to the message list
            complete_msg.label()
            cmplt_msg_list.append(complete_msg)
            parsed_beacon_queue.put(cmplt_msg_list[-1])

            # Add all other complete messages to the message list
            for i in range(1, len(new_beacon.msg_list)):
                if new_beacon.msg_list[i].partial == False:
                    complete_msg = new_beacon.msg_list[i]
                    complete_msg.label()
                    cmplt_msg_list.append(complete_msg)
                    parsed_beacon_queue.put(cmplt_msg_list[-1])


        # If previous message wasn't partial...
        else:
            # Add all complete messages to the list
            for i in range(0, len(new_beacon.msg_list)):
                if new_beacon.msg_list[i].partial == False:
                    complete_msg = new_beacon.msg_list[i]
                    complete_msg.label()
                    cmplt_msg_list.append(complete_msg)
                    parsed_beacon_queue.put(cmplt_msg_list[-1])

        if len(new_beacon.msg_list) > 0:
            # If the final message in the beacon message list is partial...
            if new_beacon.msg_list[-1].partial == True:
                # Set partial_msg to the final message in the beacon message list
                partial_msg = new_beacon.msg_list[-1]

            # Otherwise, set partial_message to none
            else:
                partial_msg = None
        
    print("Stopped parsing beacons", flush=True)