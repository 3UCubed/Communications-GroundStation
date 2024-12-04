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
from layer_1.web_socket_api.RadioConfiguration import set_radio_address, update_frequency, update_aes_key
from layer_1.web_socket_client import WebSocketClient
from layer_1.parsing.beacon_parser.realtime_beacon_parser import Beacon_Parser

import logging
import re
import os
import random
import threading
import base64
from queue import Queue
import time


# JSON Message BeaconListen
BEACON_LISTEN = {
    "id": random.randint(0, 9999),
    "type": "BeaconListen"
}

# JSON Message Beacon
BEACON = {
    "ax25Frame": [0] * 256,
    "requestId": 0,
    "type": "Beacon"
}


# @brief Sets up API used for interfacing with the OBC

obc_api = FP_API_OBC()


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

def get_filenames(pattern):
    filenames = []
    
    root_dir = os.path.dirname(__file__)
    dirlist_filepath = os.path.join(root_dir, "downloaded_files", "DIRLIST.TXT")
    with open(dirlist_filepath, 'r', encoding='ISO-8859-1') as file:
        dirlist_content = file.read()
    filenames = re.findall(pattern, dirlist_content)
    return filenames


def download_instrument_files():
    regex_pattern = "0000[0-2].(?:(?:IHK)|(?:PMT)|(?:ERP))"
    print("Downloading dirlist...")
    download_file("DIRLIST.TXT")
    filenames = get_filenames(regex_pattern)
    number_of_files = len(filenames)
    current_file_number = 1
    missed_files = []
    total_time_start = time.perf_counter()
    for file in filenames:
        start_time = time.perf_counter()
        print(f"[{current_file_number}/{number_of_files}] Downloading {file}...")
        status = download_file(file)
        retries = 0

        while retries < 10 and status == 0:
            retries += 1
            print(f"Problem downloading file, retry #{retries}")
            time.sleep(5)
            status = download_file(file)

        if status == 0:
            missed_files.append(file)

        current_file_number += 1
        end_time = time.perf_counter()
        elapsed_time = round(end_time - start_time)
        print(f"Process took {elapsed_time} seconds.")
    total_time_end = time.perf_counter()
    total_elapsed_time = round(total_time_end - total_time_start)
    print(f"Downloaded {number_of_files - len(missed_files)} of {number_of_files} files in {total_elapsed_time} seconds.")
    print("Missed files: ", end="")
    print(', '.join(missed_files))


class SPACECOMMS_INTERFACE_API:
    def __init__(self, resp_queue):
        self.resp_queue = resp_queue
        self.accepted_commands = {
            'uptime': self.get_uptime,
            'start_beacon': self.start_beacon_listening,
            'stop_beacon': self.stop_beacon_listening,
            'get_telemetry': self.download_telemetry_files,
            'shutdown': self.cleanup
        }
        self.listening_for_beacons = threading.Event()
        self.threads = {}

    def enqueue_response(self, type, data):
        response = {
            "type": type,
            "data": data
        }
        self.resp_queue.put(response)

    def command_handler(self, command):
        if command in self.accepted_commands:
            print(f"Received Command {command}")
            if command == "shutdown":
                self.cleanup()
            else:
                command_thread = threading.Thread(target=self.accepted_commands[command])
                self.threads[command] = command_thread
                command_thread.start()
        else:
            self.enqueue_response(type="error", data={"error message": "unkown command"})

    def cleanup(self):
        self.listening_for_beacons.clear()
        for command, thread in self.threads.items():
            thread.join()
            print(f"{command} has been gracefully shut down")
        
        self.threads.clear()
        print("All tasks shut down")
            
    def get_uptime(self):
        serialized_request = list(obc_api.req_getUptime())
        serialized_response = send_command(SatelliteId.DEFAULT_ID, CommandType.OBC_FP_GATEWAY, TripType.WAIT_FOR_RESPONSE, ModuleMac.OBC_MAC_ADDRESS, payload=serialized_request)
        parsed_response = obc_api.resp_getUptime(serialized_response)

        self.enqueue_response(type="uptime", data=vars(parsed_response["s__upTime"]))

        print("GET_UPTIME stopped")

    def start_beacon_listening(self):
        self.listening_for_beacons.set()
        beacon_queue = Queue()
        beacon_parser = Beacon_Parser(beacon_queue)
        message = BEACON_LISTEN
        listen_id = message["id"]
        client = WebSocketClient.WebSocketClient(enableSSL=False)
        client.send(payload_dict=message)
        while self.listening_for_beacons.is_set():
            response = {}
            response = client.readResponse()
            if response.get("type") == "Beacon":
                if listen_id != response.get("requestId"):
                    print("Mismatched ID's for beacon request")
                frame = response["ax25Frame"]
                decoded_frame = base64.b64decode(frame)
                beacon_parser.parse_beacon(decoded_frame)
                while not beacon_queue.empty():
                    parsed_beacon = beacon_queue.get()
                    self.enqueue_response(type="beacon", data=parsed_beacon)
                    
            elif response.get("type") == "Error":
                logging.error("%s", response)
                exit(0)
        client.close()
        print("START_BEACON_LISTENING stopped")

    def stop_beacon_listening(self):
        self.listening_for_beacons.clear()
        print("STOP_BEACON_LISTENING stopped")
    
    def download_telemetry_files(self):
        print("Downloading dirlist...")
        download_file("DIRLIST.TXT")
        regex_pattern = "\d{5}.TLM"
        filenames = get_filenames(regex_pattern)
        number_of_files = len(filenames)
        current_file_number = 1
        missed_files = []
        total_time_start = time.perf_counter()
        for file in filenames:
            start_time = time.perf_counter()
            print(f"[{current_file_number}/{number_of_files}] Downloading {file}...")
            status = download_file(file)
            retries = 0
            while retries < 10 and status == 0:
                retries += 1
                print(f"Problem downloading file, retry #{retries}")
                time.sleep(5)
                status = download_file(file)
            if status == 0:
                missed_files.append(file)
            current_file_number += 1
            end_time = time.perf_counter()
            elapsed_time = round(end_time - start_time)
            print(f"Process took {elapsed_time} seconds.")
        total_time_end = time.perf_counter()
        total_elapsed_time = round(total_time_end - total_time_start)
        print(f"Downloaded {number_of_files - len(missed_files)} of {number_of_files} files in {total_elapsed_time} seconds.")
        print("Missed files: ", end="")
        print(', '.join(missed_files))


