from layer_1.spacecomms_interface import SPACECOMMS_INTERFACE_API
from queue import Queue, Empty
import threading

resp_queue = Queue()
spacecomms_interface_api = SPACECOMMS_INTERFACE_API(resp_queue)


def command_resp_handler():
    while True:
        resp = resp_queue.get()
        print(resp, flush=True)


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
    
