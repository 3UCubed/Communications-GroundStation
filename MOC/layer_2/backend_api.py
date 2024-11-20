from multiprocessing import Process, Queue
from layer_1.spacecomms_interface import spacecomms_req_handler

def backend_req_handler(req_queue, resp_queue):
    print("\nEntering Backend API Command Sender")

    # Keep asking for commands while a keyboard interrupt hasn't occured
    try:
        while True:
            req = input("Enter command to send to spacecomms interface: ")
            req_queue.put(req)
            resp = resp_queue.get()
            print(resp)
    except KeyboardInterrupt:
        print("\nExiting Backend API Command Sender")

if __name__ == '__main__':
    req_queue = Queue()
    resp_queue = Queue()


    # Create and start a new process for the spacecomms interface
    spacecomms_interface_proc = Process(target=spacecomms_req_handler, args=(req_queue, resp_queue))
    spacecomms_interface_proc.start()

    # Populate req_queue 
    backend_req_handler(req_queue, resp_queue)

    # When user is done sending commands, stop the spacecomms interface process
    spacecomms_interface_proc.terminate()
    spacecomms_interface_proc.join()
    
