from layer_1.spacecomms_interface import SPACECOMMS_INTERFACE_API
from queue import Queue, Empty
import threading
from pymongo import MongoClient

resp_queue = Queue()
spacecomms_interface_api = SPACECOMMS_INTERFACE_API(resp_queue)
client = MongoClient("mongodb://localhost:27017/")
database = client["data"]


def command_resp_handler():
    while True:
        resp = resp_queue.get()
        print(resp, end="\n\n", flush=True)
        collection = database[resp["type"]]
        document = resp["data"]
        insertion_result = collection.insert_one(document)
        print(f"Insertion result: {insertion_result}")


def backend_req_handler():
    print("\nEntering Backend API Command Sender")

    # Keep asking for commands while a keyboard interrupt hasn't occured
    try:
        while True:
            command = input("Enter command to send to spacecomms interface: ")
            spacecomms_interface_api.command_handler(command)

            
    except KeyboardInterrupt:
        spacecomms_interface_api.command_handler("shutdown")
        print("\nExiting Backend API Command Sender")

if __name__ == '__main__':
    print("Starting backend API...")
    reader_thread = threading.Thread(target=command_resp_handler)
    reader_thread.daemon = True
    reader_thread.start()
    backend_req_handler()
    
