import subprocess
import os


def execute(cmd):
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    spacecomms_interface_path = os.path.join(root, "spacecomms_interface", "spacecomms_interface.py")
    beacon_listen_start_cmd = 3

    for output_line in execute(["python3", str(spacecomms_interface_path), str(beacon_listen_start_cmd)]):
        print(output_line)