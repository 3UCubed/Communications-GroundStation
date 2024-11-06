import logging
import random
from web_socket_client import WebSocketClient
import os
import base64

# JSON Message UpdateAESKey
UPDATE_AES_KEY = {
    "id": random.randint(0, 9999),
    "encrypted": True,
    "aesIV": "base64encoded",
    "aesKey": "base64encoded",
    "type": "UpdateAESKey"
}

# JSON Message UpdateRadio
UPDATE_RADIO = {
    "id": random.randint(0, 9999),
    "rfConfig": 2,
    "uplinkFrequency": 0,
    "downlinkFrequency": 0,
    "type": "UpdateRadio"
}

# JSON Message RadioConn
RADIO_CONN = {
    "id": random.randint(0, 9999),
    "remoteRadioMac": 0,
    "type": "RadioConn"
}

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

def update_aes_key(aesIV: str, aesKey: str):
    message = UPDATE_AES_KEY
    message["aesIV"] = aesIV
    message["aesKey"] = aesKey

    client = WebSocketClient.WebSocketClient(enableSSL=False)
    client.send(payload_dict=message)
    response = {}
    while response.get("type") != "RadioResult":
        response = client.readResponse()
        if response.get("type") == "Error":
            logging.error("%s", response)
            exit(0)

def update_frequency(uplinkFrequency: int, downlinkFrequency: int):
    message = UPDATE_RADIO
    message["uplinkFrequency"] = uplinkFrequency
    message["downlinkFrequency"] = downlinkFrequency

    client = WebSocketClient.WebSocketClient(enableSSL=False)
    client.send(payload_dict=message)
    response = {}
    while response.get("type") != "RadioResult":
        response = client.readResponse()
        if response.get("type") == "Error":
            logging.error("%s", response)
            exit(0)

def set_radio_address(remoteRadioMac: int):
    message = RADIO_CONN
    message["remoteRadioMac"] = remoteRadioMac

    client = WebSocketClient.WebSocketClient(enableSSL=False)
    client.send(payload_dict=message)
    response = {}
    while response.get("type") != "RadioConnResult":
        response = client.readResponse()
        if response.get("type") == "Error":
            logging.error("%s", response)
            exit(0)

def start_beacon_listening():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    filepath = os.path.join(parent_dir, "raw_beacons", "raw_beacons.bin")

    message = BEACON_LISTEN
    listen_id = message["id"]
    client = WebSocketClient.WebSocketClient(enableSSL=False)
    client.send(payload_dict=message)
    with open(filepath, "wb") as file:
        i = 0
        while i < 1:
            response = {}
            response = client.readResponse()
            if response.get("type") == "Beacon":
                if listen_id != response.get("requestId"):
                    print("Mismatched ID's for beacon request")
                frame = response["ax25Frame"]
                decoded_frame = base64.b64decode(frame)
                print(' '.join(f'{byte:02x}' for byte in decoded_frame))
                i += 1
            elif response.get("type") == "Error":
                logging.error("%s", response)
                exit(0)