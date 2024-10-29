from client_apps.OBCClientApp import FP_API_OBC
from web_socket_api.CommandProtocol import send_command
from web_socket_api.constants import SatelliteId, CommandType, TripType, ModuleMac, RadioConfiguration, EncyptionKey
from web_socket_api.RadioConfiguration import set_radio_address, update_frequency, update_aes_key
import logging
import re
import os

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
    file_format = "{0}\0".format(file_name).encode("utf-8")
    serialized_request = [0, 0, 0, 0, 0]
    serialized_request.extend(file_format)
    serialized_response = send_command(SatelliteId.DEFAULT_ID, CommandType.OBC_FILE_DOWNLOAD, TripType.WAIT_FOR_RESPONSE, ModuleMac.OBC_MAC_ADDRESS, payload=serialized_request, add_payload_length=False)
    
    with open(file_name, "wb") as file:
        file.write(serialized_response)
    
    logging.info("File {0} written to current directory".format(file_name))


# Initializing the radio
def init_radio():
    set_radio_address(ModuleMac.UHF_MAC_ADDRESS)
    update_frequency(RadioConfiguration.UHF_UPLINK_FREQUENCY, RadioConfiguration.UHF_DOWNLINK_FREQUENCY)
    update_aes_key(EncyptionKey.AES_IV, EncyptionKey.AES_KEY)


def get_filenames():
    filenames = []
    regex_pattern = "\d{5}.TLM"
    root_dir = os.path.dirname(__file__)
    dirlist_filepath = os.path.join(root_dir, "DIRLIST.TXT")
    with open(dirlist_filepath, 'r', encoding='ISO-8859-1') as file:
        dirlist_content = file.read()
    filenames = re.findall(regex_pattern, dirlist_content)
    return filenames


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # init_radio()

    # print("Getting Uptime...")
    # get_uptime()

    print("Downloading dirlist...")
    download_file("DIRLIST.TXT")

    filenames = get_filenames()
    number_of_files = len(filenames)
    current_file_number = 1
    for file in filenames:
        print(f"[{current_file_number}/{number_of_files}] Downloading {file}...")
        retries = 0
        response = None
        while retries < 10 and response is None:
            response = download_file(file)
            print(response)
            if response is not None:
                print("Success")
                break
            retries += 1
            print(f"Retry #{retries}")

        current_file_number += 1
