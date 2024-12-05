from layer_1.spacecomms_interface import SPACECOMMS_INTERFACE_API
from queue import Queue, Empty
import threading
from pymongo import MongoClient

resp_queue = Queue()
spacecomms_interface_api = SPACECOMMS_INTERFACE_API(resp_queue)
client = MongoClient("mongodb://localhost:27017/")
database = client["data"]


# @brief Handles responses from the response queue and inserts them into the database.
# 
# @details Continuously retrieves responses from the queue, processes them based on
#          their type, and inserts the corresponding data into the appropriate database
#          collection. If the response type is "telemetry", it inserts multiple documents,
#          otherwise, a single document is inserted.

def command_resp_handler():
    while True:
        resp = resp_queue.get()
        # print(resp, end="\n\n", flush=True)
        collection = database[resp["type"]]
        document = resp["data"]
        if resp["type"] == "telemetry":
            print(f"\n\nDocument to insert: {document}")
            insertion_result = collection.insert_many(document)
        else:
            insertion_result = collection.insert_one(document)
        print(f"Insertion result: {insertion_result}")


# @brief Handles user input for sending commands to the spacecomms interface.
# 
# @details Continuously prompts the user to enter commands, sending each one
#          to the spacecomms interface for processing. On keyboard interrupt,
#          sends a "shutdown" command and exits the function.

def backend_req_handler():
    print("\nEntering Backend API Command Sender")

    try:
        while True:
            command = input("Enter command to send to spacecomms interface: ")
            spacecomms_interface_api.command_handler(command)

    except KeyboardInterrupt:
        spacecomms_interface_api.command_handler("shutdown")
        print("\nExiting Backend API Command Sender")


# @brief Starts the backend API and initializes the reader thread.
# 
# @details Creates a new thread to handle command responses and starts the
#          backend request handler. The reader thread is set as a daemon thread
#          to run in the background.

if __name__ == '__main__':
    print("Starting backend API...")
    reader_thread = threading.Thread(target=command_resp_handler)
    reader_thread.daemon = True
    reader_thread.start()
    backend_req_handler()
    
