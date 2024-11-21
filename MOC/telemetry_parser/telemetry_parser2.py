from sys import argv
import datetime
import os
from struct import unpack_from
from rich import print
from dependencies import es_crc
from dependencies import cobs
from dependencies import datacache
import csv
import glob
from itertools import islice
from typing import List
# Variable controlling how many tasks are in the TaskStats vector
NUM_TASKS = 30


# -----------------------------------------------------------------------------------------------------------
def unixtime_to_readable_date(unix_timestamp: int) -> str:
    date_string = ""

    try:
        date_string = datetime.datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as exc:
        date_string = "invalid timestamp"

    return date_string

# -----------------------------------------------------------------------------------------------------------
class TelemetryMsg:
    HDR_SIZE = 11
    CRC_SIZE = 2
    MAX_TLM_ROLL_FRAME_CNT = 256

    def __init__(self, msg_id: int):
        self.timestamp = ''
        self.rolling_cntr = 0
        self.obc_opmode = 0
        self.msg_type = 0
        self.frame_counter = 0
        self.tlm_data_status = False
        self.data = []
        self.data_len = 0
        self.crc = 0
        self.calc_crc = 0
        self.is_crc_valid = False
        self.total_len = 0
        self.msg_id = msg_id
        self.str_from_parsed_dict = ''
        self.parsed_data = None  # Initialize parsed_data here

    def set_frame_counter(self, counter: int):
        self.frame_counter = counter  # Method to set the frame counter

    def _print_reply(self, dict_mac_reply, ident=8):
        """
        Helper function to print parsed data recursively in a structured format
        """
        str_space_val = "  ".ljust(ident)
        for key, value in dict_mac_reply.items():
            if (type(value) is list and "libs.mac" in str(value)) or (
                type(value) is list and "libs.fidl" in str(value)
            ):
                for item in value:
                    attribute_dict = vars(item)
                    self._print_reply(attribute_dict, ident + 2)
            else:
                self.str_from_parsed_dict += f"{str_space_val}{key:<22}:           {value}\n"

    def parse(self, data: bytes) -> int:
        if len(data) < TelemetryMsg.HDR_SIZE:
            self.total_len = 0
            return 0

        # Unpack the header part of the data
        (
            self.timestamp,
            self.rolling_cntr,
            self.obc_opmode,
            self.msg_type,
            self.tlm_data_status,
            self.data_len,
        ) = unpack_from("<LBBHBH", data)

        # Create a dictionary to hold parsed data
        self.parsed_data = {
            "timestamp": self.timestamp,
            "rolling_cntr": self.rolling_cntr,
            "obc_opmode": self.obc_opmode,
            "msg_type": self.msg_type,
            "tlm_data_status": self.tlm_data_status,
            "data_len": self.data_len,
            "data": []  # Will hold the parsed data bytes
        }

        # Extract the actual data from the message (after the header)
        for b in data[TelemetryMsg.HDR_SIZE : TelemetryMsg.HDR_SIZE + self.data_len]:
            self.parsed_data["data"].append(b)

        # Extract CRC and calculate the validity
        self.crc = unpack_from(
            "<H",
            data[TelemetryMsg.HDR_SIZE + self.data_len : TelemetryMsg.HDR_SIZE + self.data_len + TelemetryMsg.CRC_SIZE]
        )[0]

        # Skip CRC bytes for calculation
        self.calc_crc = es_crc.crc_util.crc16(data[: -TelemetryMsg.CRC_SIZE])

        self.is_crc_valid = (self.crc == self.calc_crc)

        self.total_len = TelemetryMsg.HDR_SIZE + self.data_len + TelemetryMsg.CRC_SIZE

        return self.total_len if self.is_crc_valid else 0

    def is_valid(self) -> bool:
        """
        Returns whether the telemetry message is valid based on CRC.
        """
        return self.is_crc_valid

    def deserialize(self, parser, verbose: bool = True) -> str:
        """
        Deserialize the telemetry message's data if it's valid.
        """
        printout: str = ""

        # Deserialize the data only if it exists
        if len(self.parsed_data["data"]) > 0:
            (deser_data, bytes_cnt) = parser.parse_by_id(self.msg_type, self.parsed_data["data"])
            printout = f'deserialized data [{bytes_cnt}] -> [{deser_data}]' + os.linesep

            if verbose:
                # Print the parsed data structure if available
                self._print_reply(deser_data.__dict__)
                printout += self.str_from_parsed_dict + os.linesep
                self.str_from_parsed_dict = ''

        return printout

    def __str__(self):
        """
        Return a string representation of the telemetry message for logging.
        """
        str_repr = (f'{self.msg_id} => TelemetryMsgHdr> [{self.total_len}] timestamp: {self.timestamp} | '
                    f'rollcntr: {self.rolling_cntr} | obc_opmode: {self.obc_opmode} | msg_type: {hex(self.msg_type)} | '
                    f'data_status: {self.tlm_data_status} | len: {self.data_len} | crc: {self.crc} | '
                    f'is_crc_valid: {self.is_crc_valid} | calc_crc: {self.calc_crc}')
        return str_repr

# -----------------------------------------------------------------------------------------------------------

class TelemetryFileHdr:
    HDR_SIZE = 21  # Adjust if the header size is different
    CRC_SIZE = 2   # Assuming CRC is 2 bytes

    def __init__(self):
        self.signature = ''
        self.version = 0
        self.next_write_offset = 0
        self.last_timestamp = 0
        self.file_complete = False
        self.crc = 0
        self.calc_crc = 0
        self.is_crc_valid = False
        self.frame_counter = 0  # Initialize frame counter

    def parse(self, data: bytes, msg: TelemetryMsg) -> int:
        """
        Parse the telemetry header, validate CRC, check data completeness,
        and extract the frame counter (if available in the header).

        Args:
            data (bytes): The raw bytes of the telemetry header.
            msg (TelemetryMsg): The message object to store frame counter

        Returns:
            int: The number of bytes read if the header is valid, otherwise 0.
        """
        # Check if the data length is sufficient to unpack the header
        if len(data) >= TelemetryFileHdr.HDR_SIZE:
            try:
                # Unpack the header data from the byte stream
                (
                    self.signature,
                    self.version,
                    self.next_write_offset,
                    self.last_timestamp,
                    self.file_complete,
                    self.crc,
                ) = unpack_from("<6sLLL?H", data)

                # Calculate CRC and check if it matches
                self.calc_crc = es_crc.crc_util.crc16(data[: -TelemetryFileHdr.CRC_SIZE])
                self.is_crc_valid = (self.crc == self.calc_crc)

                # Extract frame counter from the data (adjust location as necessary)
                if len(data) > TelemetryFileHdr.HDR_SIZE:
                    # Assuming the frame counter is stored right after the header (adjust if needed)
                    self.frame_counter = data[TelemetryFileHdr.HDR_SIZE]  # Example frame counter location
                    msg.set_frame_counter(self.frame_counter)  # Set the frame counter in the message object

                # Return the number of bytes read if the header is valid
                if self.is_crc_valid:
                    return TelemetryFileHdr.HDR_SIZE
                else:
                    print("Warning: Invalid CRC in telemetry header.")
                    return 0  # Invalid CRC

            except Exception as e:
                print(f"Error unpacking telemetry header: {e}")
                return 0  # Return 0 if unpacking fails

        else:
            print("Error: Insufficient data to unpack telemetry header.")
            return 0  # Insufficient data

    def is_valid(self) -> bool:
        """
        Returns whether the header's CRC is valid.

        Returns:
            bool: True if CRC is valid, otherwise False.
        """
        return self.is_crc_valid

    def __str__(self):
        """
        Return a string representation of the telemetry header for logging.

        Returns:
            str: A string describing the telemetry header's details.
        """
        return (
            f'TelemetryFileHdr> signature: {self.signature} | ver: {self.version} | '
            f'next_write_offset: {self.next_write_offset} | last_timestamp: {self.last_timestamp} | '
            f'complete: {self.file_complete} | crc: {hex(self.crc)} | is_valid: {self.is_crc_valid} | '
            f'calc_crc: {hex(self.calc_crc)} | frame_counter: {self.frame_counter}'
        )


# -----------------------------------------------------------------------------------------------------------
class CSVFiles:
    # Class Attributes
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
        0x00000035: "ADCS_4"
    }

    # Initialization
    def __init__(self, msglist: List, input_filename: str):
        self.msglist = msglist
        self.input_filename = input_filename

        # Automatically generate the output folder path based on the input TLM file
        self.output_folderpath = self.generate_output_folderpath(input_filename)

        # Example: output file will be the parsed data in the "csv_files" folder
        self.output_filepath = os.path.join(self.output_folderpath, "parsed_data.csv")

    @staticmethod
    def generate_output_folderpath(input_file: str) -> str:
        """
        Generates the output folder path based on the TLM input file name.
        Ensures that the directory exists.
        """
        root_dir = os.path.dirname(__file__)
        folder_name = os.path.basename(input_file).split('.')[0]  # Use base filename as folder name
        output_folderpath = os.path.join(root_dir, "csv_files", folder_name)

        # Create the output folder if it doesn't already exist
        os.makedirs(output_folderpath, exist_ok=True)
        return output_folderpath

    def generate_output_filepath(self, msg_type: str) -> str:
        """
        Generates the file path for a specific message type.
        Example: returns a path like 'csv_files/001/parsed_data.csv'.
        """
        # Generate the filename (based on message type or other logic)
        file_name = f"{msg_type}.csv"
        return os.path.join(self.output_folderpath, file_name)

    def write_header(self, parsed_data: dict) -> None:
        """
        Write the header to the CSV file.
        This is done once when creating the file.
        """
        header = ['timestamp'] + list(parsed_data.keys())

        if not os.path.exists(self.output_filepath):
            with open(self.output_filepath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                print(f"Header written to {self.output_filepath}")
        else:
            print(f"File {self.output_filepath} already exists, skipping header write.")

    def generate_csv_files(self):
        """
        Generate CSV files by processing messages, ensuring dropped frames are handled.
        """
        previous_frame_counter = None  # Initialize to track frame sequence

        # Process and append each message's parsed data
        for msg in self.msglist:
            # Handle dropped frames (if frame counter is missing or out-of-order)
            if previous_frame_counter is not None:
                if msg.frame_counter != previous_frame_counter + 1:
                    # If the current frame counter is not sequential, it's a dropped frame
                    print(f"Dropped frame detected: expected {previous_frame_counter + 1}, but got {msg.frame_counter}. Skipping this message.")
                    continue  # Skip this message and move to the next one
        
            # Check if parsed_data exists (handle missing data gracefully)
            if not hasattr(msg, 'parsed_data') or msg.parsed_data is None:
                print(f"Warning: Message {msg.frame_counter} does not have parsed_data. Skipping message.")
                continue  # Skip this message if parsed_data is missing or invalid

            # Proceed with appending the data if parsed_data is valid
            parsed_data = msg.parsed_data
            self.append_data(msg, parsed_data)

            # Update the frame counter for the next iteration
            previous_frame_counter = msg.frame_counter

        # Optionally write the header (if it's the first time writing)
        if not os.path.exists(self.output_filepath):
            # Assuming the first message provides the header structure
            self.write_header(self.msglist[0].parsed_data)  # Write the header for CSV


    
    # Parses message data using datacache parser
    @staticmethod
    def parse_msg_data(msg):
        (data, length) = datacache.dc_parser(NUM_TASKS).parse_by_id(msg.msg_type, msg.data)
        data_dict = data.__dict__

        if CSVFiles.dc_entries_dict[msg.msg_type] == "ADCS_0":
            data_dict = CSVFiles.parse_adcs_0_vec(data_dict)
        elif CSVFiles.dc_entries_dict[msg.msg_type] == "ADCS_1":
            data_dict = CSVFiles.parse_adcs_1_vec(data_dict)
        elif CSVFiles.dc_entries_dict[msg.msg_type] == "ADCS_2":
            data_dict = CSVFiles.parse_adcs_2_vec(data_dict)
        elif CSVFiles.dc_entries_dict[msg.msg_type] == "AOCS_CNTRL_TLM":
            data_dict = CSVFiles.parse_aocs_cntrl_tlm_vec(data_dict)
        elif CSVFiles.dc_entries_dict[msg.msg_type] == "EPS_3": # Hasn't been tested, tlm files don't have this right now
            data_dict = CSVFiles.parse_eps_3_vec(data_dict)
        elif CSVFiles.dc_entries_dict[msg.msg_type] == "EPS_4": # Hasn't been tested, tlm files don't have this right now
            data_dict = CSVFiles.parse_eps_4_vec(data_dict)
        elif CSVFiles.dc_entries_dict[msg.msg_type] == "TaskStats":
            data_dict = CSVFiles.parse_taskstats_vec(data_dict)

        return data_dict
    

    @staticmethod
    def parse_adcs_0_vec(data_dict):
        new_dict = {}
        new_keys = []
        new_values = []

        for key, value in data_dict.items():
            if key == 'a__int16__magFieldVec':
                new_keys += ['magFieldVec_X', 'magFieldVec_Y', 'magFieldVec_Z']
            elif key == 'a__int16__coarseSunVec':
                new_keys += ['coarseSunVec_X', 'coarseSunVec_Y', 'coarseSunVec_Z']
            elif key == 'a__int16__fineSunVec':
                new_keys += ['fineSunVec_X', 'fineSunVec_Y', 'fineSunVec_Z']
            elif key == 'a__int16__nadirVec':
                new_keys += ['nadirVec_X', 'nadirVec_Y', 'nadirVec_Z']
            elif key == 'a__int16__angRateVec':
                new_keys += ['angRateVec_X', 'angRateVec_Y', 'angRateVec_Z']
            elif key == 'a__int16__wheelSpeedArr':
                new_keys += ['wheelSpeedArr_X', 'wheelSpeedArr_Y', 'wheelSpeedArr_Z']

            new_values += [value[0], value[1], value[2]]
            new_dict.update({key: value for key, value in zip(new_keys, new_values)})

        return new_dict

    @staticmethod
    def parse_adcs_1_vec(data_dict):
        new_dict = {}
        new_keys = []
        new_values = []
        for key, value in data_dict.items():
            if key == 'a__int16__estQSet':
                new_keys += ['estQSet_Q1', 'estQSet_Q2', 'estQSet_Q3']
            elif key == 'a__int16__estAngRateVec':
                new_keys += ['estQSet_X', 'estQSet_Y', 'estQSet_Z']

            new_values += [value[0], value[1], value[2]]
            new_dict.update({key: value for key, value in zip(new_keys, new_values)})

        return new_dict
    
    @staticmethod
    def parse_adcs_2_vec(data_dict):
        vector_data = data_dict['a__uint8__adcsState']

        new_dict = {
            'Attitude_Estimation_Mode': 0,
            'Control_Mode': 0,
            'ADCS_Run_Mode': 0,
            'ASGP4_Mode': 0,
            'CubeControl_Signal_Enabled': 0,
            'CubeControl_Motor_Enabled': 0,
            'CubeSense1_Enabled': 0,
            'CubeSense2_Enabled': 0,
            'CubeWheel1_Enabled': 0,
            'CubeWheel2_Enabled': 0,
            'CubeWheel3_Enabled': 0,
            'CubeStar_Enabled': 0,
            'GPS_Receiver_Enabled': 0,
            'GPS_LNA_Power_Enabled': 0,
            'Motor_Driver_Enabled': 0,
            'Sun_is_Above_Local_Horizon': 0,
            'CubeSense1_Communications_Error': 0,
            'CubeSense2_Communications_Error': 0,
            'CubeControl_Signal_Communications_Error': 0,
            'CubeControl_Motor_Communications_Error': 0,
            'CubeWheel1_Communications_Error': 0,
            'CubeWheel2_Communications_Error': 0,
            'CubeWheel3_Communications_Error': 0,
            'CubeStar_Communications_Error': 0,
            'Magnetometer_Range_Error': 0,
            'Cam1_SRAM_Overcurrent_Detected': 0,
            'Cam1_3V3_Overcurrent_Detected': 0,
            'Cam1_Sensor_Busy_Error': 0,
            'Cam1_Sensor_Detection_Error': 0,
            'Sun_Sensor_Range_Error': 0,
            'Cam2_SRAM_Overcurrent_Detected': 0,
            'Cam2_3V3_Overcurrent_Detected': 0,
            'Cam2_Sensor_Busy_Error': 0,
            'Cam2_Sensor_Detection_Error': 0,
            'Nadir_Sensor_Range_Error': 0,
            'Rate_Sensor_Range_Error': 0,
            'Wheel_Speed_Range_Error': 0,
            'Coarse_Sun_Sensor_Error': 0,
            'StarTracker_Match_Error': 0,
            'StarTracker_Overcurrent_Detected': 0
        }

        byte_0 = vector_data[0]
        byte_1 = vector_data[1]
        byte_2 = vector_data[2]
        byte_3 = vector_data[3]
        byte_4 = vector_data[4]
        byte_5 = vector_data[5]

        # Bits 0-7
        # 01 00 10 11
        new_dict['Attitude_Estimation_Mode'] = byte_0 & 0b1111  # 10 11
        new_dict['Control_Mode'] = (byte_0 >> 4) & 0b1111       # 01 00    
        
        # Bits 8-15
        # 01 00 10 11
        new_dict['ADCS_Run_Mode'] = byte_1 & 0b1                        # 1
        new_dict['ASGP4_Mode'] = (byte_1 >> 1) & 0b1                    # 1
        new_dict['CubeControl_Signal_Enabled'] = (byte_1 >> 2) & 0b1    # 0
        new_dict['CubeControl_Motor_Enabled'] = (byte_1 >> 3) & 0b1     # 1
        new_dict['CubeSense1_Enabled'] = (byte_1 >> 4) & 0b11           # 00
        new_dict['CubeSense2_Enabled'] = (byte_1 >> 6) & 0b11           # 01

        # Bits 16-23
        # 01 00 10 11
        new_dict['CubeWheel1_Enabled'] = byte_2 & 0b1                   # 1
        new_dict['CubeWheel2_Enabled'] = (byte_2 >> 1) & 0b1            # 1
        new_dict['CubeWheel3_Enabled'] = (byte_2 >> 2) & 0b1            # 0
        new_dict['CubeStar_Enabled'] = (byte_2 >> 3) & 0b1              # 1
        new_dict['GPS_Receiver_Enabled'] = (byte_2 >> 4) & 0b1          # 0
        new_dict['GPS_LNA_Power_Enabled'] = (byte_2 >> 5) & 0b1         # 0
        new_dict['Motor_Driver_Enabled'] = (byte_2 >> 6) & 0b1          # 1
        new_dict['Sun_is_Above_Local_Horizon'] = (byte_2 >> 7) & 0b1    # 0

        # Bits 24-31
        # 01 00 10 11
        new_dict['CubeSense1_Communications_Error'] = byte_3 & 0b1                  # 1
        new_dict['CubeSense2_Communications_Error'] = (byte_3 >> 1) & 0b1           # 1
        new_dict['CubeControl_Signal_Communications_Error'] = (byte_3 >> 2) & 0b1   # 0
        new_dict['CubeControl_Motor_Communications_Error'] = (byte_3 >> 3) & 0b1    # 1
        new_dict['CubeWheel1_Communications_Error'] = (byte_3 >> 4) & 0b1           # 0
        new_dict['CubeWheel2_Communications_Error'] = (byte_3 >> 5) & 0b1           # 0
        new_dict['CubeWheel3_Communications_Error'] = (byte_3 >> 6) & 0b1           # 1
        new_dict['CubeStar_Communications_Error'] = (byte_3 >> 7) & 0b1             # 0

        # Bits 32-39
        # 01 00 10 11
        new_dict['Magnetometer_Range_Error'] = byte_4 & 0b1                 # 1
        new_dict['Cam1_SRAM_Overcurrent_Detected'] = (byte_4 >> 1) & 0b1    # 1
        new_dict['Cam1_3V3_Overcurrent_Detected'] = (byte_4 >> 2) & 0b1     # 0
        new_dict['Cam1_Sensor_Busy_Error'] = (byte_4 >> 3) & 0b1            # 1
        new_dict['Cam1_Sensor_Detection_Error'] = (byte_4 >> 4) & 0b1       # 0
        new_dict['Sun_Sensor_Range_Error'] = (byte_4 >> 5) & 0b1            # 0
        new_dict['Cam2_SRAM_Overcurrent_Detected'] = (byte_4 >> 6) & 0b1    # 1
        new_dict['Cam2_3V3_Overcurrent_Detected'] = (byte_4 >> 7) & 0b1     # 0

        # Bits 40-47
        # 01 00 10 11
        new_dict['Cam2_Sensor_Busy_Error'] = byte_5 & 0b1                   # 1
        new_dict['Cam2_Sensor_Detection_Error'] = (byte_5 >> 1) & 0b1       # 1
        new_dict['Nadir_Sensor_Range_Error'] = (byte_5 >> 2) & 0b1          # 0
        new_dict['Rate_Sensor_Range_Error'] = (byte_5 >> 3) & 0b1           # 1
        new_dict['Wheel_Speed_Range_Error'] = (byte_5 >> 4) & 0b1           # 0
        new_dict['Coarse_Sun_Sensor_Error'] = (byte_5 >> 5) & 0b1           # 0
        new_dict['StarTracker_Match_Error'] = (byte_5 >> 6) & 0b1           # 1
        new_dict['StarTracker_Overcurrent_Detected'] = (byte_5 >> 7) & 0b1  # 0

        return new_dict



    @staticmethod
    def parse_aocs_cntrl_tlm_vec(data_dict):
        new_dict = {}
        new_keys = []
        new_values = []
        for key, value in data_dict.items():
            if key == 'uint16__adcsErrFlags':
                new_keys.append('adcsErrFlags')
                new_values.append(value)
            elif key == 'int32__estAngRateNorm':
                new_keys.append('estAngRateNorm')
                new_values.append(value)
            elif key == 'a__int32__estAngRateVec':
                new_keys += ['estAngRateVec_X', 'estAngRateVec_Y', 'estAngRateVec_Z']
                new_values += [value[0], value[1], value[2]]
            elif key == 'a__int32__estAttAngles':
                new_keys += ['estAttAngles_Roll', 'estAttAngles_Pitch', 'estAttAngles_Yaw']
                new_values += [value[0], value[1], value[2]]
            elif key == 'a__int16__measWheelSpeed':
                new_keys += ['measWheelSpeed_X', 'measWheelSpeed_Y', 'measWheelSpeed_Z']
                new_values += [value[0], value[1], value[2]]

            new_dict.update({key: value for key, value in zip(new_keys, new_values)})
        return new_dict


    @staticmethod
    def parse_eps_3_vec(data_dict):
        new_dict = {}
        new_keys = []
        new_values = []
        for key, value in data_dict.items():
            if key == 'int16__VOLT_BRDSUP':
                new_keys.append('VOLT_BRDSUP')
                new_values.append(value)
            elif key == 'int16__TEMP_MCU':
                new_keys.append('TEMP_MCU')
                new_values.append(value)
            elif key == 'int16__VIP_INPUT_Voltage':
                new_keys.append('VIP_INPUT_Voltage')
                new_values.append(value)
            elif key == 'int16__VIP_INPUT_Current':
                new_keys.append('VIP_INPUT_Current')
                new_values.append(value)
            elif key == 'int16__VIP_INPUT_Power':
                new_keys.append('VIP_INPUT_Power')
                new_values.append(value)
            elif key == 'uint16__STAT_BU':
                new_keys.append('STAT_BU')
                new_values.append(value)
            elif key == 'a__int16__VIP_BP_INPUT_Voltage':
                new_keys += ['BP_INPUT_Voltage_1', 'BP_INPUT_Voltage_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__VIP_BP_INPUT_Current':
                new_keys += ['BP_INPUT_Current_1', 'BP_INPUT_Current_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__VIP_BP_INPUT_Power':
                new_keys += ['BP_INPUT_Power_1', 'BP_INPUT_Power_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__STAT_BP':
                new_keys += ['STAT_BP_1', 'STAT_BP_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__VOLT_CELL1':
                new_keys += ['VOLT_CELL1_1', 'VOLT_CELL1_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__VOLT_CELL2':
                new_keys += ['VOLT_CELL2_1', 'VOLT_CELL2_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__VOLT_CELL3':
                new_keys += ['VOLT_CELL3_1', 'VOLT_CELL3_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__VOLT_CELL4':
                new_keys += ['VOLT_CELL4_1', 'VOLT_CELL4_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__BAT_TEMP1':
                new_keys += ['BAT_TEMP1_1', 'BAT_TEMP1_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__BAT_TEMP2':
                new_keys += ['BAT_TEMP2_1', 'BAT_TEMP2_2']
                new_values += [value[0], value[1]]
            elif key == 'a__int16__BAT_TEMP3':
                new_keys += ['BAT_TEMP3_1', 'BAT_TEMP3_2']
                new_values += [value[0], value[1]]

            new_dict.update({key: value for key, value in zip(new_keys, new_values)})

        return new_dict


    @staticmethod
    def parse_eps_4_vec(data_dict):
        new_dict = {}
        new_keys = []
        new_values = []
        for key, value in data_dict.items():
            if key == 'int16__VOLT_BRDSUP':
                new_keys.append('VOLT_BRDSUP')
                new_values.append(value)
            elif key == 'int16__TEMP_MCU':
                new_keys.append('TEMP_MCU')
                new_values.append(value)
            elif key == 'int16__VIP_OUTPUT_Voltage':
                new_keys.append('VIP_OUTPUT_Voltage')
                new_values.append(value)
            elif key == 'int16__VIP_OUTPUT_Current':
                new_keys.append('VIP_OUTPUT_Current')
                new_values.append(value)
            elif key == 'int16__VIP_OUTPUT_Power':
                new_keys.append('VIP_OUTPUT_Power')
                new_values.append(value)
            elif key == 'a__int16__VIP_CC_OUTPUT_Voltage':
                new_keys += ['VIP_CC_OUTPUT_Voltage_1', 'VIP_CC_OUTPUT_Voltage_2', 'VIP_CC_OUTPUT_Voltage_3', 'VIP_CC_OUTPUT_Voltage_4']
                new_values += [value[0], value[1], value[2], value[3]]
            elif key == 'a__int16__VIP_CC_OUTPUT_Current':
                new_keys += ['VIP_CC_OUTPUT_Current_1', 'VIP_CC_OUTPUT_Current_2', 'VIP_CC_OUTPUT_Current_3', 'VIP_CC_OUTPUT_Current_4']
                new_values += [value[0], value[1], value[2], value[3]]
            elif key == 'a__int16__VIP_CC_OUTPUT_Power':
                new_keys += ['VIP_CC_OUTPUT_Power_1', 'VIP_CC_OUTPUT_Power_2', 'VIP_CC_OUTPUT_Power_3', 'VIP_CC_OUTPUT_Power_4']
                new_values += [value[0], value[1], value[2], value[3]]
            elif key == 'a__int16__CCx_VOLT_IN_MPPT':
                new_keys += ['VOLT_IN_MPPT_1', 'VOLT_IN_MPPT_2', 'VOLT_IN_MPPT_3', 'VOLT_IN_MPPT_4']
                new_values += [value[0], value[1], value[2], value[3]]
            elif key == 'a__int16__CCx_CURR_IN_MPPT':
                new_keys += ['CURR_IN_MPPT_1', 'CURR_IN_MPPT_2', 'CURR_IN_MPPT_3', 'CURR_IN_MPPT_4']
                new_values += [value[0], value[1], value[2], value[3]]
            elif key == 'a__int16__CCx_VOLT_OU_MPPT':
                new_keys += ['VOLT_OU_MPPT_1', 'VOLT_OU_MPPT_2', 'VOLT_OU_MPPT_3', 'VOLT_OU_MPPT_4']
                new_values += [value[0], value[1], value[2], value[3]]
            elif key == 'a__int16__CCx_CURR_OU_MPPT':
                new_keys += ['CURR_OU_MPPT_1', 'CURR_OU_MPPT_2', 'CURR_OU_MPPT_3', 'CURR_OU_MPPT_4']
                new_values += [value[0], value[1], value[2], value[3]]

            new_dict.update({key: value for key, value in zip(new_keys, new_values)})

        return new_dict


    @staticmethod
    def parse_taskstats_vec(data_dict):
        new_dict = {
            'TASK_MONITOR_TASK': 0,
            'TASK_MONITOR_EXEH_PERSISTOR': 0,
            'TASK_MONITOR_APP_TASK': 0,
            'TASK_MONITOR_SERVICES': 0,
            'TASK_MONITOR_SD_MANAGER': 0,
            'TASK_INSTRUMENTS': 0,
            'TASK_MONITOR_S_X_BAND': 0,
            'TASK_MONITOR_CUBEADCS': 0,
            'TASK_MONITOR_CUBEADCS_FHANDL': 0,
            'TASK_MONITOR_GNSS': 0,
            'TASK_PAYLOAD_SCHEDULER': 0,
            'TASK_TELEMETRY': 0,
            'TASK_TELEMETRY_FILE_SINK': 0,
            'TASK_MONITOR_SP': 0,
            'TASK_MACDRV_DISPATCHER': 0,
            'TASK_MACTL_DISPATCHER': 0,
            'TASK_FWUPD_HANDLER': 0,
            'TASK_ESSA_SP_HANDLER': 0,
            'TASK_NVM': 0,
            'TASK_DATACACHE': 0,
            'TASK_ADCS_TLM': 0,
            'TASK_CONOPS_PERIODIC_EV': 0,
            'TASK_MONITOR_PAYLOAD_CTRL': 0,
            'TASK_BEACONS': 0,
            'TASK_EPS_CTRL': 0,
            'TASK_EPS_I': 0,
            'TASK_EPS_II': 0,
            'TASK_EPS_M': 0,
            'TASK_SYS_CLOCK': 0,
            'TASK_MONITOR_ES_ADCS': 0,
            'TASK_ACTUATOR_CONTROL_SERVICE': 0,
            'TASK_SDS': 0,
            'TASK_AOCS_CNTRL': 0,
            'TASK_SXBAND_SCHED': 0,
            'TASK_CRYPTO_SRV': 0,
            'TASK_MONITOR_TASKS_NUMBER': 0
        }

        vector_data = data_dict['a__int16__taskStackMaxUnusedSize']

        if NUM_TASKS == 30:
            for key, value in zip(islice(new_dict.keys(), NUM_TASKS), vector_data):
                new_dict[key] = value
            new_dict = dict(islice(new_dict.items(), NUM_TASKS))
        elif NUM_TASKS == 36:
            for key, value in zip(new_dict.keys(), vector_data):
                new_dict[key] = value
        else:
            return data_dict
        
        return new_dict

    # Creates CSV file and writes the headers
    @staticmethod
    def write_header(parsed_data, output_filepath):
        header = ['timestamp']
        header += list(parsed_data.keys())

        # Check if the file already exists
        if os.path.exists(output_filepath):
            # If the file exists, do not write the header again
            print(f"File {output_filepath} already exists, skipping header write.")
        else:
            # If the file does not exist, create it and write the header
            with open(output_filepath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                print(f"Header written to {output_filepath}")
    
    # Appends parsed data to CSV file
    @staticmethod
    def append_data(msg, parsed_data, output_filepath):
        row = []
        readable_timestamp = unixtime_to_readable_date(msg.timestamp)  # Assuming this function exists
        row.append(readable_timestamp)

        # Add parsed data values
        for value in parsed_data.values():
            row.append(value)

        # Check if the file already exists and if it's empty
        if os.path.exists(output_filepath):
            # Check if the file is empty (only check the first line to determine if it's empty)
            with open(output_filepath, mode='r', newline='') as file:
                first_line = file.readline()
                if not first_line:  # File is empty, write header
                    print(f"File is empty, writing header to {output_filepath}")
                    header = ['timestamp'] + list(parsed_data.keys())  # Assuming `parsed_data` contains the keys
                    with open(output_filepath, mode='w', newline='') as write_file:
                        writer = csv.writer(write_file)
                        writer.writerow(header)
                        writer.writerow(row)  # Write the first row of data
                        print(f"Header and data written to {output_filepath}")
                else:
                    # If the file is not empty, just append the data
                    with open(output_filepath, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row)
                        print(f"Data appended to {output_filepath}")
        else:
            # If the file doesn't exist, create it and write the data (header + row)
            print(f"File does not exist, creating and writing data to {output_filepath}")
            header = ['timestamp'] + list(parsed_data.keys())  # Assuming `parsed_data` contains the keys
            with open(output_filepath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerow(row)
                print(f"Data written to {output_filepath}")


# -----------------------------------------------------------------------------------------------------------
class TelemetryFile:
    def __init__(self, fname: str):
        script_dir = os.path.dirname(__file__)
        self.fname = os.path.join(script_dir, "tlm_files", fname)
        self.msglist = []
        self.invalid_msg_cnt = 0

    def parse_file(self, output_filepath: str) -> None:
        """
        Make sure output_filepath is passed to this function when it's called.
        """
        # Create an instance of TelemetryFileHdr
        fhdr = TelemetryFileHdr()

        # Open the file in binary read mode
        with open(self.fname, "rb") as f:
            # Parse the header of the telemetry file
            header_data = f.read(TelemetryFileHdr.HDR_SIZE)
            fhdr.parse(header_data, None)

            print(fhdr)

            byte = f.read(1)
            msgdata = []
            msg_idx = 0
            prev_rollling_cntr = 0
            first_frame = True

            while byte:
                current_pos = f.tell()

                if byte[0] != 0:
                    msgdata.append(byte[0])
                else:
                    msgdata.append(0)
                    msg = TelemetryMsg(msg_idx)
                    msg_idx += 1

                    try:
                        decoded_data = cobs.decode(msgdata)
                        msg.parse(decoded_data)

                        if not msg.is_crc_valid:
                            self.invalid_msg_cnt += 1
                            print(f"Invalid message CRC: {msg_idx}")

                        if first_frame:
                            prev_rollling_cntr = msg.rolling_cntr
                            first_frame = False
                        else:
                            if ((prev_rollling_cntr + 1) % TelemetryMsg.MAX_TLM_ROLL_FRAME_CNT) != msg.rolling_cntr:
                                print('\n...\n:exclamation_mark: [bold red]dropped frames[/bold red]\n...\n')

                        prev_rollling_cntr = msg.rolling_cntr

                        self.msglist.append(msg)

                        # Assuming msg contains parsed data, prepare it for CSV writing
                        parsed_data = msg.parsed_data
                        if output_filepath:
                            CSVFiles.append_data(msg, parsed_data, output_filepath)
                        else:
                            print("Error: output_filepath not provided")
                            return

                    except Exception as exc:
                        print(f'Oops: Could not parse record -> {exc}')

                    msgdata = []

                byte = f.read(1)

        print(f'{len(self.msglist)} messages parsed | invalid count: {self.invalid_msg_cnt}')


# -----------------------------------------------------------------------------------------------------------
# Usage: Place all .TLM files to be parsed in the 'tlm_files' directory. 
# For each parsed .TLM file, a corresponding folder will be created inside 
# the 'csv_files' directory, where the generated CSV files will be stored.
if __name__ == "__main__":
    root_dir = os.path.dirname(__file__)
    tlm_file_list = glob.glob(f"{root_dir}/tlm_files/*.TLM")
    for file in tlm_file_list:
        try:
            # Create a TelemetryFile object
            tlm_file = TelemetryFile(file)
            
            # Define the output file path dynamically (use the base name of the TLM file)
            output_filepath = f"{os.path.splitext(os.path.basename(file))[0]}_output.csv"  # Output CSV file name based on TLM file name
            
            # Call parse_file and pass the output_filepath argument
            tlm_file.parse_file(output_filepath)

            # Create an instance of CSVFiles and generate CSV
            file_handler = CSVFiles(tlm_file.msglist, tlm_file.fname)
            file_handler.generate_csv_files()

        except Exception as exc:
            print(f'Oops: {exc}')
        except KeyboardInterrupt:
            print("Program interrupted")