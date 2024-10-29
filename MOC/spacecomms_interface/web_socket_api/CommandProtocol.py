import base64
import logging
import random
from web_socket_client import WebSocketClient

# JSON Message CPCommand
CP = {
    "id": random.randint(0, 9999),
    "cmdId": random.randint(0, 9999),
    "satId": "0",
    "moduleMac": 0,
    "payload": [0],
    "readTimeout": "999s",
    "writeTimeout": "999s",
    "noProgressTimeout": "5s",
    "cmdType": 9999,
    "tripType": 1,
    "type": "CPCommand"
}  

def send_command(satId: int, commandType: int, tripType: int, moduleMac: int, payload: list, add_payload_length: bool = True):
    message = CP
    message["satId"] = satId
    message["cmdType"] = commandType
    message["tripType"] = tripType
    message["moduleMac"] = moduleMac

    if add_payload_length:
        payload = [len(payload)] + payload
    message["payload"] = payload

    client = WebSocketClient.WebSocketClient(enableSSL=False)
    client.send(payload_dict=message)
    response = {}
    while response.get("type") != "CPCommandResult":         # Continue reading from the websocket until CPCommandResult message arrives
        response = client.readResponse()
        if response.get("type") == "Error":
            logging.error("%s", response)
            print("Error, retrying...")
            return None
    #        exit(0)

    response = base64.b64decode(response["payload"].encode("ascii"))
    return response
