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

def unixtime_to_readable_date(unix_timestamp: int) -> str:
    date_string = ""

    try:
        date_string = datetime.datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as exc:
        date_string = "invalid timestamp"

    return date_string


class TelemetryFileHdr:
    HDR_SIZE = 21
    CRC_SIZE = 2

    def __init__(self):
        self.signature = ''
        self.version = 0
        self.next_write_offset = 0
        self.last_timestamp = 0
        self.file_complete = False
        self.crc = 0
        self.calc_crc = 0
        self.is_crc_valid = False

    def parse(self, data: bytes) -> int:
        if len(data) >= TelemetryFileHdr.HDR_SIZE:
            (
                self.signature,
                self.version,
                self.next_write_offset,
                self.last_timestamp,
                self.file_complete,
                self.crc,
            ) = unpack_from("<6sLLL?H", data)
            # skip CRC bytes...
            self.calc_crc = es_crc.crc_util.crc16(data[: -TelemetryFileHdr.CRC_SIZE])

            self.is_crc_valid = (self.crc == self.calc_crc)

            return TelemetryFileHdr.HDR_SIZE if self.is_crc_valid else 0
        else:
            return 0

    def is_valid(self) -> bool:
        return self.is_crc_valid

    def __str__(self):
        return f'TelemetryFileHdr> signature: {self.signature} | ver: {self.version} | next_write_offset: {self.next_write_offset} | last_timestamp: {self.last_timestamp} | complete: {self.file_complete} | crc: {hex(self.crc)} | is_valid: {self.is_crc_valid} | calc_crc: {hex(self.calc_crc)}'


class TelemetryMsg:
    HDR_SIZE = 11
    CRC_SIZE = 2
    MAX_TLM_ROLL_FRAME_CNT = 256

    def __init__(self, msg_id: int):
        self.timestamp = ''
        self.rolling_cntr = 0
        self.obc_opmode = 0
        self.msg_type = 0
        self.tlm_data_status = False
        self.data = []
        self.data_len = 0
        self.crc = 0
        self.calc_crc = 0
        self.is_crc_valid = False
        self.total_len = 0
        self.msg_id = msg_id
        self.str_from_parsed_dict = ''

    def _print_reply(self, dict_mac_reply, ident=8):
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

        # Unpack the data
        (
            self.timestamp,
            self.rolling_cntr,
            self.obc_opmode,
            self.msg_type,
            self.tlm_data_status,
            self.data_len,
        ) = unpack_from("<LBBHBH", data)

        for b in data[TelemetryMsg.HDR_SIZE : TelemetryMsg.HDR_SIZE + self.data_len]:
            self.data.append(b)

        self.crc = unpack_from(
            "<H",
            data[TelemetryMsg.HDR_SIZE + self.data_len : TelemetryMsg.HDR_SIZE + self.data_len + TelemetryMsg.CRC_SIZE]
        )[0]

        # skip CRC bytes...
        self.calc_crc = es_crc.crc_util.crc16(data[: -TelemetryMsg.CRC_SIZE])

        self.is_crc_valid = (self.crc == self.calc_crc)

        self.total_len = TelemetryMsg.HDR_SIZE + self.data_len + TelemetryMsg.CRC_SIZE

        return (self.total_len) if self.is_crc_valid else 0

    def is_valid(self) -> bool:
        return self.is_crc_valid

    def deserialize(self, parser, verbose: bool = True) -> str:
        printout: str = ""

        # Deserialize the data only if there is any
        if len(self.data) > 0:
            (deser_data, bytes_cnt) = parser.parse_by_id(self.msg_type, self.data)
            printout = f'deserialized data [{bytes_cnt}] -> [{deser_data}]' + os.linesep

            if verbose:
                self._print_reply(deser_data.__dict__)
                printout += (self.str_from_parsed_dict) + os.linesep
                self.str_from_parsed_dict = ''

        return printout

    # def __str__(self):
    #     str_repr = f'{self.msg_id} => TelemetryMsgHdr> [{self.total_len}] timestamp: {unixtime_to_readable_date(self.timestamp)} | rollcntr: {self.rolling_cntr} | obc_opmode: {self.obc_opmode} | msg_type: {hex(self.msg_type)} | data_status: {self.tlm_data_status} | len: {self.data_len} | crc: {self.crc} | is_crc_valid: {self.is_crc_valid} | calc_crc: {self.calc_crc}'
    #     str_repr = str_repr + os.linesep + "\t" + self.deserialize(datacache.dc_parser())

    #     return str_repr


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
    def __init__(self, msglist, input_file):
        self.msglist = msglist
        self.output_folderpath = CSVFiles.generate_output_folderpath(input_file)
            
    # Public user function
    def generate_csv_files(self):
        for msg in self.msglist:
            if len(msg.data) > 0:
                parsed_data = CSVFiles.parse_msg_data(msg)
                output_filepath = self.generate_output_filepath(msg)
                file_exists = os.path.exists(output_filepath)

                if not file_exists:
                    CSVFiles.write_header(parsed_data, output_filepath)

                CSVFiles.append_data(msg, parsed_data, output_filepath)

    # Generates output folderpath given input TLM file name
    @staticmethod
    def generate_output_folderpath(input_file):
        root_dir = os.path.dirname(__file__)
        folder_name = os.path.basename(input_file).split('.')[0]
        output_folderpath = os.path.join(root_dir, "csv_files", folder_name)
        os.makedirs(output_folderpath, exist_ok=False)
        print(output_folderpath)
        return output_folderpath
    
    # Generates output filepath given message type
    def generate_output_filepath(self, msg):
        file_name = CSVFiles.dc_entries_dict[msg.msg_type] + ".csv"
        output_filepath = os.path.join(self.output_folderpath, file_name)
        return output_filepath
    
    # Parses message data using datacache parser
    @staticmethod
    def parse_msg_data(msg):
        (data, length) = datacache.dc_parser().parse_by_id(msg.msg_type, msg.data)
        return data.__dict__
    
    # Creates CSV file and writes the headers
    @staticmethod
    def write_header(parsed_data, output_filepath):
        header = ['timestamp']
        header += list(parsed_data.keys())

        with open(output_filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    
    # Appends parsed data to CSV file
    @staticmethod
    def append_data(msg, parsed_data, output_filepath):
                row = []
                readable_timestamp = unixtime_to_readable_date(msg.timestamp)
                row.append(readable_timestamp)

                for value in parsed_data.values():
                    row.append(value)

                with open(output_filepath, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row)


class TelemetryFile:
    def __init__(self, fname: str):
        script_dir = os.path.dirname(__file__)
        self.fname = os.path.join(script_dir, "tlm_files", fname)
        self.msglist = []
        self.invalid_msg_cnt = 0

    def parse_file(self) -> None:
        fhdr = TelemetryFileHdr()

        f = open(self.fname, "rb")

        fhdr.parse(f.read(TelemetryFileHdr.HDR_SIZE))

        print(fhdr)

        byte = f.read(1)
        msgdata = []
        msg_idx = 0
        prev_rollling_cntr = 0
        first_frame = False

        while byte:
            current_pos = f.tell()

            if byte[0] != 0:
                msgdata.append(byte[0])
            else:
                msgdata.append(0)
                msg = TelemetryMsg(msg_idx)
                msg_idx += 1

                try:
                    msg.parse(cobs.decode(msgdata))
                except Exception as exc:
                    print(f'Oops: Could not parse record -> {exc}')

                if not msg.is_crc_valid:
                    self.invalid_msg_cnt += 1

                if first_frame:
                    prev_rollling_cntr = msg.rolling_cntr
                    first_frame = False
                else:
                    if ((prev_rollling_cntr + 1) % TelemetryMsg.MAX_TLM_ROLL_FRAME_CNT) != msg.rolling_cntr:
                        print('\n...\n:exclamation_mark: [bold red]dropped frames[/bold red]\n...\n')

                prev_rollling_cntr = msg.rolling_cntr

                self.msglist.append(msg)

                # Deserialize data and append deser data to the list after the message itself

                msgdata = []

            byte = f.read(1)

        f.close()
        print(f'{len(self.msglist)} messages parsed | invalid count: {self.invalid_msg_cnt}')


if __name__ == "__main__":
    root_dir = os.path.dirname(__file__)
    tlm_file_list = glob.glob(f"{root_dir}/tlm_files/*.TLM")
    for file in tlm_file_list:
        try:
            tlm_file = TelemetryFile(file)
            tlm_file.parse_file()

            file_handler = CSVFiles(tlm_file.msglist, tlm_file.fname)
            file_handler.generate_csv_files()

        except Exception as exc:
            print(f'Oops: {exc}')
        except KeyboardInterrupt:
            print("Program interrupted")