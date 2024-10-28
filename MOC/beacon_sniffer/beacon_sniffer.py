import subprocess
from sys import argv
import re
import binascii
from struct import *
from time import time
from rich import print
import datetime


def execute(cmd):
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


class BeaconMsgHdr:
    HDR_SIZE = 4
    INVALID_BEACON_SLOT_ASSIGNMENT = 0xFFFF

    def __init__(self):
        self.bcn_type = BeaconMsgHdr.INVALID_BEACON_SLOT_ASSIGNMENT
        self.data_status = 0
        self.len = 0

    def parse(self, data: bytes) -> int:
        if len(data) >= BeaconMsgHdr.HDR_SIZE:
            self.bcn_type, self.data_status, self.len = unpack_from(
                "HBB", data)

            return BeaconMsgHdr.HDR_SIZE
        else:
            return 0

    def is_valid(self) -> bool:
        return self.bcn_type != BeaconMsgHdr.INVALID_BEACON_SLOT_ASSIGNMENT

    def __str__(self):
        return f'BeaconMsgHdr> bcn_type: {self.bcn_type} | status: {self.data_status} | len: {self.len}'


class BeaconMessage:
    def __init__(self, parent: 'BeaconFrame'):
        self.hdr = None
        self.data = bytes()
        self.partial_message = False
        self.parent = parent

    def parse_message(self, msg_data: bytes) -> int:
        bytes_parsed = 0

        self.hdr = BeaconMsgHdr()
        hdr_bytes = self.hdr.parse(msg_data)

        if (self.hdr.is_valid()):
            self.data = msg_data[hdr_bytes: hdr_bytes + self.hdr.len]

            self.partial_message = len(self.data) < self.hdr.len

            bytes_parsed = hdr_bytes + len(self.data)

        return bytes_parsed

    def append_data(self, msg: 'BeaconMessage') -> tuple:
        if (msg.hdr.bcn_type == self.hdr.bcn_type) and (msg.parent == self.parent):
            self.data += msg.data

            self.partial_message = (len(self.data) == self.hdr.len)

            # tuple(result of append, is message still partial)
            return (True, self.partial_message)
        else:
            return (False, self.partial_message)

    def __str__(self):
        return f'BeaconMsg> [ {self.hdr} ] => {len(self.data)}: {binascii.hexlify(self.data)}'


class BeaconFrameHdr:
    HDR_SIZE = 3
    BEACON_FRAME_FLAG_CONTINUATION = 0x01

    def __init__(self):
        self.bcn_number = 0
        self.op_mode = 0
        self.flags = 0

    def parse(self, data: bytes) -> int:
        if len(data) >= BeaconFrameHdr.HDR_SIZE:
            (self.bcn_number, self.op_mode, self.flags) = unpack_from("BBB", data)

            return BeaconFrameHdr.HDR_SIZE
        else:
            return 0

    def is_split_frame(self) -> bool:
        return self.flags & BeaconFrameHdr.BEACON_FRAME_FLAG_CONTINUATION

    def __str__(self):
        return f'BeaconFrmHdr> bcn_number: {self.bcn_number} | op_mode: {self.op_mode} | split: {self.is_split_frame()}'


class BeaconFrame:
    BCN_FRAME_SIZE = 73

    def __init__(self):
        self.hdr = None
        self.beacon_messages: list[BeaconMessage] = []
        self.is_split_frame = False
        self.timestamp: 'datetime.time' = None

    def parse_beacon_frame(self, timestamp: 'datetime.time', frame_data: bytes) -> bool:
        self.timestamp = timestamp
        offset = 0
        msg_count_in_frame = 0

        # parse beacon frame header
        self.hdr = BeaconFrameHdr()

        offset += self.hdr.parse(frame_data)

        self.is_split_frame = self.hdr.is_split_frame()

        # parse individual messages in the frame
        while (offset < len(frame_data)):
            bcn_msg = BeaconMessage(self)

            bytes_parsed = bcn_msg.parse_message(frame_data[offset:])

            if bytes_parsed > 0:
                msg_count_in_frame += 1

                offset += bytes_parsed

                self.beacon_messages.append(bcn_msg)
            else:
                break

        return msg_count_in_frame > 0

    def time_to_us(ts1: datetime.time, ts2: datetime.time):
        milliseconds_diff = (ts1.microsecond / 1000) + \
            (ts1.hour * 3600 + ts1.minute * 60 + ts1.second) * 1000
        milliseconds_diff -= (ts2.microsecond / 1000) + \
            (ts2.hour * 3600 + ts2.minute * 60 + ts2.second) * 1000

        return datetime.timedelta(milliseconds=milliseconds_diff)

    def get_delta_from_frame(self, bcn_frame: 'BeaconFrame'):
        return BeaconFrame.time_to_us(self.timestamp, bcn_frame.timestamp)

    def __str__(self):
        bcn_str = f'{self.timestamp} BeaconFrame> [ {self.hdr} ] => msg_cnt = {len(self.beacon_messages)}\n'

        msg_idx = 0
        for bcn_msg in self.beacon_messages:
            bcn_str += f'\t[{msg_idx}] => {bcn_msg}\n'
            msg_idx += 1

        return bcn_str


class BeaconSniffer:
    MAX_BCN_NUMBER = 256

    def __init__(self):
        self.beacon_frames_list: list[BeaconFrame] = []
        self.partial_frames: list[BeaconFrame] = []
        self.last_rcvd_beacon_number = 0

    def parse_beacon_frame(self, timestamp: datetime.time, frame_data: bytes) -> bool:
        bcn_frm = BeaconFrame()
        parse_result = bcn_frm.parse_beacon_frame(timestamp, frame_data)

        if parse_result:
            if (len(self.beacon_frames_list) > 0):
                print(
                    f':down_arrow: {bcn_frm.get_delta_from_frame(self.beacon_frames_list[-1])} :down_arrow: ')

            self.beacon_frames_list.append(bcn_frm)

            if bcn_frm.is_split_frame:
                self.partial_frames.append(bcn_frm)

            if ((self.last_rcvd_beacon_number + 1) % BeaconSniffer.MAX_BCN_NUMBER) != bcn_frm.hdr.bcn_number:
                print(
                    '\n...\n:exclamation_mark: [bold red]dropped frames[/bold red]\n...\n')

            print(bcn_frm)

            self.last_rcvd_beacon_number = bcn_frm.hdr.bcn_number

        return parse_result

    def process_partial_frames(self):
        combined_msg_size = 0
        last_partial_msg = None

        for frame in self.partial_frames:
            for msg in frame.beacon_messages:
                if msg.partial_message:
                    # new partial message
                    if last_partial_msg == None:
                        last_partial_msg = msg
                    else:
                        (append_res, msg_still_partial) = last_partial_msg.append_data(msg)

                        if append_res:
                            if not msg_still_partial:
                                print(
                                    f'partial message restored: {last_partial_msg}\n')
                                last_partial_msg = None

        if last_partial_msg == None:
            print(f'Partial messages still remain in the list...')


def parse_timestamp(ts: str) -> 'datetime.time':
    timestamp = datetime.time.fromisoformat(ts)

    return timestamp


sniffer = BeaconSniffer()

for output_line in execute([argv[1]]):
    m = re.search(
        "(\d\d:\d\d:\d\d\.\d{3}).*?\[00\] \[11\] \[33\] \[0C\] \[6C\] : (.*?)$", output_line)

    if m != None:
        # print(f'size = {len(m.group(1))}, value = {m.group(1)}')
        ts = parse_timestamp(m.group(1))
        data = binascii.unhexlify(m.group(2))

        FP_HDR_SIZE = 10

        if (len(data) > FP_HDR_SIZE):
            # start from byte #10 skipping FP header...
            if not sniffer.parse_beacon_frame(
                    ts, data[FP_HDR_SIZE:BeaconFrame.BCN_FRAME_SIZE + FP_HDR_SIZE]):
                print(
                    f':exclamation_mark: {ts} empty or invalid frame => [{m.group(2)}]')
