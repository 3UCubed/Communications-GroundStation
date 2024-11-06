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



if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    spacecomms_interface_path = os.path.join(root, "spacecomms_interface", "spacecomms_interface.py")
    beacon_listen_start_cmd = 3

    for output_line in execute(["python3", str(spacecomms_interface_path), str(beacon_listen_start_cmd)]):
        print(output_line)