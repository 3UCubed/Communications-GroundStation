import os

class BeaconFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse_file(self):
        file = open(self.filepath, "rb")
        byte = file.read(1)
        while byte:
            print(f"{byte[0]:02x}", end=" ")
            byte = file.read(1)

if __name__ == "__main__":
    root = os.path.dirname(__file__)
    filepath = os.path.join(root, "raw_beacons.bin")
    beacons = BeaconFile(filepath)
    beacons.parse_file()
