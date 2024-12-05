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
from layer_1.parsing.telemetry_parser.telemetry_parser import Unpacker, TelemetryFile
import logging
import re
import os
import random
import threading
import base64
from queue import Queue
import time
import glob

BEACON_LISTEN = {
    "id": random.randint(0, 9999),
    "type": "BeaconListen"
}
BEACON = {
    "ax25Frame": [0] * 256,
    "requestId": 0,
    "type": "Beacon"
}
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
# @return A list of filenames matching the pattern.

def get_filenames(pattern):
    filenames = []
    
    root_dir = os.path.dirname(__file__)
    dirlist_filepath = os.path.join(root_dir, "downloaded_files", "DIRLIST.TXT")
    with open(dirlist_filepath, 'r', encoding='ISO-8859-1') as file:
        dirlist_content = file.read()
    filenames = re.findall(pattern, dirlist_content)
    return filenames


# @brief Initializes the SPACECOMMS_INTERFACE_API class.
# 
# @details Sets up the response queue, command mappings, and initializes internal
#          variables such as the beacon listening event and a dictionary to store
#          active threads. The accepted commands are mapped to their corresponding
#          handler methods.
# 
# @param resp_queue Queue for receiving responses to be processed by the API.

class SPACECOMMS_INTERFACE_API:


# @brief Initializes the SPACECOMMS_INTERFACE_API class with command mappings and internal state.
# 
# @details Sets up the response queue, maps accepted commands to their corresponding handler methods,
#          and initializes variables for beacon listening and managing threads. This sets the initial state
#          for handling various space communication tasks.
# 
# @param resp_queue Queue for receiving and processing responses.

    def __init__(self, resp_queue):
        self.resp_queue = resp_queue
        self.accepted_commands = {
            'uptime': self.get_uptime,
            'start_beacon': self.start_beacon_listening,
            'stop_beacon': self.stop_beacon_listening,
            'get_telemetry': self.download_telemetry_files,
            'get_instrument': self.download_instrument_files,
            'get_dirlist': self.download_dirlist,
            'parse_telemetry': self.parse_telemetry,
            'shutdown': self.cleanup
        }
        self.listening_for_beacons = threading.Event()
        self.threads = {}


# @brief Enqueues a response to the response queue.
# 
# @details Creates a response dictionary with the specified type and data, then
#          adds it to the response queue for further processing.
# 
# @param type The type of the response (e.g., 'telemetry').
# @param data The data associated with the response.

    def enqueue_response(self, type, data):
        response = {
            "type": type,
            "data": data
        }
        self.resp_queue.put(response)


# @brief Handles incoming commands and initiates the corresponding actions.
# 
# @details Checks if the received command is in the accepted commands list. If it is,
#          it starts a new thread to handle the command. If the command is "shutdown",
#          it calls the cleanup method. If the command is not recognized, an error response
#          is enqueued with an "unknown command" message.
# 
# @param command The command to be processed.

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


# @brief Cleans up resources and shuts down all running tasks.
# 
# @details Clears the beacon listening event, waits for all threads to complete,
#          and prints a shutdown message for each command. Clears the threads dictionary
#          after all tasks are shut down and prints a final shutdown message.

    def cleanup(self):
        self.listening_for_beacons.clear()
        for command, thread in self.threads.items():
            thread.join()
            print(f"{command} has been gracefully shut down")
        
        self.threads.clear()
        print("All tasks shut down")


# @brief Retrieves the uptime of the onboard computer (OBC).
# 
# @details Sends a request to the OBC to get the uptime, waits for the response,
#          parses the response, and enqueues it for processing. The response data
#          is extracted from the parsed response and sent as an "uptime" type.

    def get_uptime(self):
        serialized_request = list(obc_api.req_getUptime())
        serialized_response = send_command(SatelliteId.DEFAULT_ID, CommandType.OBC_FP_GATEWAY, TripType.WAIT_FOR_RESPONSE, ModuleMac.OBC_MAC_ADDRESS, payload=serialized_request)
        parsed_response = obc_api.resp_getUptime(serialized_response)

        self.enqueue_response(type="uptime", data=vars(parsed_response["s__upTime"]))

        print("GET_UPTIME stopped")


# @brief Starts listening for beacons from the WebSocket client.
# 
# @details Initializes the beacon listening process by setting up a WebSocket client,
#          sending a beacon listen message, and continuously reading responses. When a
#          beacon response is received, it decodes the AX.25 frame and parses the beacon data.
#          The parsed beacons are enqueued for further processing. If an error response is received,
#          the process is terminated. The listening process continues until the beacon listening flag is cleared.

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


# @brief Stops the beacon listening process.
# 
# @details Clears the beacon listening flag, effectively stopping the listening loop
#          and halting any further beacon processing.

    def stop_beacon_listening(self):
        self.listening_for_beacons.clear()
        print("STOP_BEACON_LISTENING stopped")
    

# @brief Downloads telemetry files from the server.
# 
# @details Downloads the directory listing file (DIRLIST.TXT), retrieves the filenames
#          matching the telemetry file pattern, and attempts to download each file.
#          If a download fails, it retries up to 10 times with a 5-second delay between attempts.
#          It tracks the number of files successfully downloaded and logs any missed files.
# 
# @note The total time taken for the download process is also recorded and displayed.

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


# @brief Parses telemetry files and generates JSON data.
# 
# @details Retrieves all telemetry files in the "downloaded_files" directory, parses
#          each file, and generates JSON data from the parsed telemetry messages. 
#          The resulting JSON data is enqueued for further processing.

    def parse_telemetry(self):
        root_dir = os.path.dirname(__file__)
        tlm_file_list = glob.glob(f"{root_dir}/downloaded_files/*.TLM")
        for file in tlm_file_list:
            tlm_file = TelemetryFile(file)
            tlm_file.parse_file()
            file_handler = Unpacker(tlm_file.msglist, tlm_file.fname)
            json_data = file_handler.generate_json_data()
            self.enqueue_response(type="telemetry", data=json_data)


# @brief Downloads instrument-related files based on a specific pattern.
# 
# @details Downloads the directory listing (DIRLIST.TXT) and retrieves filenames matching
#          a regex pattern for instrument files (IHK, PMT, ERP). Each file is downloaded,
#          with up to 10 retries in case of failure. The number of successfully downloaded files
#          and any missed files are tracked and displayed along with the time taken for the process.

    def download_instrument_files(self):
        # Get 21 to 42
        regex_pattern = "(?:000(?:(?:2[1-9])|(?:3[0-9])|(?:4[0-2]))).(?:(?:IHK)|(?:PMT)|(?:ERP))"
        print("Downloading dirlist...")
        download_file("DIRLIST.TXT")
        filenames = get_filenames(regex_pattern)
        print(filenames)
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


# @brief Downloads the directory listing file (DIRLIST.TXT).
# 
# @details Initiates the download of the DIRLIST.TXT file and logs the download status.

    def download_dirlist(self):
        print("Downloading dirlist...")
        download_file("DIRLIST.TXT")
        print("Downloaded Dirlist", end="\n\n")
