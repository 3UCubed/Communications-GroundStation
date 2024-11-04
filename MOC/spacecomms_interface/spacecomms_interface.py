from client_apps.OBCClientApp import FP_API_OBC
from web_socket_api.CommandProtocol import send_command
from web_socket_api.constants import SatelliteId, CommandType, TripType, ModuleMac, RadioConfiguration, EncyptionKey
from web_socket_api.RadioConfiguration import set_radio_address, update_frequency, update_aes_key, start_beacon_listening
import logging
import re
import os
import time

# For API containing OBC commands
obc_api = FP_API_OBC()


# Gets uptime from OBC through SpaceComms
def get_uptime():
    serialized_request = list(obc_api.req_getUptime())
    serialized_response = send_command(SatelliteId.DEFAULT_ID, CommandType.OBC_FP_GATEWAY, TripType.WAIT_FOR_RESPONSE, ModuleMac.OBC_MAC_ADDRESS, payload=serialized_request)
    parsed_response = obc_api.resp_getUptime(serialized_response)
    logging.info(vars(parsed_response["s__upTime"]))


# Downloads a file given a filename
def download_file(file_name: str):
    status = 1
    file_format = "{0}\0".format(file_name).encode("utf-8")
    serialized_request = [0, 0, 0, 0, 0]
    serialized_request.extend(file_format)
    serialized_response = send_command(SatelliteId.DEFAULT_ID, CommandType.OBC_FILE_DOWNLOAD, TripType.WAIT_FOR_RESPONSE, ModuleMac.OBC_MAC_ADDRESS, payload=serialized_request, add_payload_length=False)

    if serialized_response is None:
        status = 0
        return status
    root = os.path.dirname(__file__)
    file_path = os.path.join(root, "downloaded_files", file_name)
    with open(file_path, "wb") as file:
        file.write(serialized_response)
    
    logging.info("File {0} written to current directory".format(file_name))
    return status

# Initializing the radio
def init_radio():
    set_radio_address(ModuleMac.UHF_MAC_ADDRESS)
    update_frequency(RadioConfiguration.UHF_UPLINK_FREQUENCY, RadioConfiguration.UHF_DOWNLINK_FREQUENCY)
    update_aes_key(EncyptionKey.AES_IV, EncyptionKey.AES_KEY)


def get_filenames():
    filenames = []
    regex_pattern = "\d{5}.TLM"
    root_dir = os.path.dirname(__file__)
    dirlist_filepath = os.path.join(root_dir, "downloaded_files", "DIRLIST.TXT")
    with open(dirlist_filepath, 'r', encoding='ISO-8859-1') as file:
        dirlist_content = file.read()
    filenames = re.findall(regex_pattern, dirlist_content)
    return filenames

def download_telemetry_files():
    print("Downloading dirlist...")
    download_file("DIRLIST.TXT")

    filenames = get_filenames()
    number_of_files = len(filenames)
    current_file_number = 1
    missed_files = []
    total_time_start = time.perf_counter()
    for file in filenames:
        start_time = time.perf_counter()
        print(f"[{current_file_number}/{number_of_files}] Downloading {file}...")
        status = download_file(file)
        retries = 0

        while retries <= 10 and status == 0:
            retries += 1
            print(f"Problem downloading file, retry #{retries}")
            time.sleep(5)
            status = download_file(file)

        if status == 0:
            missed_files += file

        current_file_number += 1
        end_time = time.perf_counter()
        elapsed_time = round(end_time - start_time)
        print(f"Process took {elapsed_time} seconds.")
    total_time_end = time.perf_counter()
    total_elapsed_time = round(total_time_end - total_time_start)
    print(f"Downloaded {number_of_files - len(missed_files)} of {number_of_files} files in {total_elapsed_time} seconds.")
    print("Missed files: ", end="")
    print(', '.join(missed_files))
    

def print_menu():
    print(f"\n1  ------------  Get Uptime")
    print(f"2  ------------  Download TLM files")
    print(f"3  ------------  Start beacon listener")
    print(f"4  ------------  Quit")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_radio()

    print_menu()
    cmd = input("\nEnter a command... ")
    if cmd == "1":
        get_uptime()
    elif cmd == "2":
        download_telemetry_files()
    elif cmd == "3":
        start_beacon_listening()
    else:
        exit(0)