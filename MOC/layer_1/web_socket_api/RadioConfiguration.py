import logging
import random
from layer_1.web_socket_client import WebSocketClient
import threading

beacon_listening_event = threading.Event()

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


