 ##############################################################################
 # @file           : spacecomms_interface.py
 # @author 		   : Jared Morrison
 # @date	 	   : November 18, 2024
 # @brief          : Interfaces with SpaceComms. Can be used to retreive
 #                   uptime, download all .TLM files, and start beacon
 #                   listening.
 ##############################################################################


from layer_1.client_apps.OBCClientApp import FP_API_OBC
from layer_1.web_socket_api.CommandProtocol import send_command
from layer_1.web_socket_api.constants import SatelliteId, CommandType, TripType, ModuleMac, RadioConfiguration, EncyptionKey
from layer_1.web_socket_api.RadioConfiguration import set_radio_address, update_frequency, update_aes_key, start_beacon_listening, stop_beacon_listening
import logging
import re
import os
import time
import sys


# @brief Sets up API used for interfacing with the OBC

obc_api = FP_API_OBC()




# @brief Retrieves the uptime of the satellite.
# 
# @details This function sends a request to the OBC to get the satellite's uptime,
#          waits for the response, parses it, and logs the parsed uptime value.
# 
# @return None

def get_uptime():
    serialized_request = list(obc_api.req_getUptime())
    serialized_response = send_command(SatelliteId.DEFAULT_ID, CommandType.OBC_FP_GATEWAY, TripType.WAIT_FOR_RESPONSE, ModuleMac.OBC_MAC_ADDRESS, payload=serialized_request)
    parsed_response = obc_api.resp_getUptime(serialized_response)
    logging.info(vars(parsed_response["s__upTime"]))
    return parsed_response


# @brief Downloads a file from the onboard computer.
# 
# @details This function sends a file download request to the onboard computer (OBC) using the provided 
#          filename, waits for the response, and writes the received file data to the local disk.
# 
# @param file_name The name of the file to download.
# @return Returns 1 if the file was successfully downloaded, 0 if an error occurred.

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
    
    print(f"File {file_name} written to downloaded_files directory")
    return status


# @brief Initializes the radio with the specified configuration.
# 
# @details This function sets the radio's MAC address, updates the uplink and downlink frequencies, 
#          and configures the AES encryption key for secure communication.
# 
# @return None

def init_radio():
    set_radio_address(ModuleMac.UHF_MAC_ADDRESS)
    update_frequency(RadioConfiguration.UHF_UPLINK_FREQUENCY, RadioConfiguration.UHF_DOWNLINK_FREQUENCY)
    update_aes_key(EncyptionKey.AES_IV, EncyptionKey.AES_KEY)


# @brief Retrieves a list of filenames matching the specified pattern.
# 
# @details This function reads the DIRLIST.TXT file from the "downloaded_files" directory, searches for
#          filenames that match the regex pattern, and returns a list of those filenames.
# 
# @return A list of filenames matching the pattern "\d{5}.TLM".

def get_filenames():
    filenames = []
    regex_pattern = "\d{5}.TLM"
    root_dir = os.path.dirname(__file__)
    dirlist_filepath = os.path.join(root_dir, "downloaded_files", "DIRLIST.TXT")
    with open(dirlist_filepath, 'r', encoding='ISO-8859-1') as file:
        dirlist_content = file.read()
    filenames = re.findall(regex_pattern, dirlist_content)
    return filenames


# @brief Downloads telemetry files listed in DIRLIST.TXT.
# 
# @details This function downloads the DIRLIST.TXT file, extracts the filenames of the telemetry files,
#          and attempts to download each file. If a download fails, it retries up to 10 times before marking
#          the file as missed. The function also tracks the time taken for each file and the overall download process.
# 
# @return None

def download_telemetry_files():
    # print("Downloading dirlist...")
    # download_file("DIRLIST.TXT")

    # filenames = get_filenames()
    # number_of_files = len(filenames)
    # current_file_number = 1
    # missed_files = []
    # total_time_start = time.perf_counter()
    # for file in filenames:
    #     start_time = time.perf_counter()
    #     print(f"[{current_file_number}/{number_of_files}] Downloading {file}...")
    #     status = download_file(file)
    #     retries = 0

    #     while retries < 10 and status == 0:
    #         retries += 1
    #         print(f"Problem downloading file, retry #{retries}")
    #         time.sleep(5)
    #         status = download_file(file)

    #     if status == 0:
    #         missed_files.append(file)

    #     current_file_number += 1
    #     end_time = time.perf_counter()
    #     elapsed_time = round(end_time - start_time)
    #     print(f"Process took {elapsed_time} seconds.")
    # total_time_end = time.perf_counter()
    # total_elapsed_time = round(total_time_end - total_time_start)
    # print(f"Downloaded {number_of_files - len(missed_files)} of {number_of_files} files in {total_elapsed_time} seconds.")
    # print("Missed files: ", end="")
    # print(', '.join(missed_files))
    return f"{__name__}: Downloaded TLM"
    


COMMANDS = {
     "GET_UPTIME": get_uptime,
     "DOWNLOAD_TELEMETRY": download_telemetry_files,
     "START_BEACON_LISTENING": start_beacon_listening,
     "STOP_BEACON_LISTENING": stop_beacon_listening
}

def spacecomms_req_handler(req_queue, resp_queue):
    while True:
        req = req_queue.get()
        if req in COMMANDS:
            resp = COMMANDS[req]()
            resp_queue.put(resp)
        else:
            resp_queue.put(f"{__name__}: Unknown Command")
