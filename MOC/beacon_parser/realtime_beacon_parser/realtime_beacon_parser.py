import subprocess
import os


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


class Beacon:
    def __init__(self, data: bytes):
        # self.beacon_header = BeaconHeader()
        self.message_list = []
        self.data = data

    def parse(self):
        # self.beacon_header.parse()
        print(self.data)

    



if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    spacecomms_interface_path = os.path.join(root, "spacecomms_interface", "spacecomms_interface.py")
    beacon_listen_start_cmd = 3

    for output_line in execute(["python3", str(spacecomms_interface_path), str(beacon_listen_start_cmd)]):
        print(output_line)
        byte_data = bytes.fromhex(output_line)
        new_beacon = Beacon(byte_data)
        new_beacon.parse()