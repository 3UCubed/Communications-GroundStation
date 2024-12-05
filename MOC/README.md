# Description
Backend of the MOC used to accept commands from openMCT.

# Quick-Start
Ensure SpaceComms is running

Open a terminal in your documents directory, or wherever you keep your git repos

Clone the repository: ```git clone https://github.com/3UCubed/Communications-GroundStation.git```

Change directory into the repo: ```cd Communications-GroundStation/MOC/```

Start the backend API: ```python3 -m layer_2.backend_api```

#### Note: Commands should all be entered in the terminal running backend API, even when there is output being printed to it. It can always accept a new command even if it is currently running a different command.

## I want to... Download all telemetry files from the OBC
In the terminal running the backend API, enter command ```get_telemetry```

## I want to... Parse all of the telemetry files I downloaded
In the terminal running the backend API, enter command ```parse_telemetry```

## I want to... Parse beacon data in real-time
In the terminal running the backend API, enter command ```start_beacon```


# Directory Structure
```
Communications Groundstation/
└── MOC/
    ├── layer_1/
    │   ├── client_apps/
    │   │   ├── OBCClientApp.py
    │   │   └── SerDesHelpers.py
    │   ├── downloaded_files/
    │   ├── parsing/
    │   │   ├── beacon_parser/
    │   │   │   └── realtime_beacon_parser
    │   │   └── telemetry_parser/
    │   │       ├── csv_files/
    │   │       ├── dependencies/
    │   │       │   ├── cobs.py
    │   │       │   ├── datacache.py
    │   │       │   └── es_crc.py
    │   │       ├── tlm_files
    │   │       ├── SerDesHelpers.py
    │   │       └── telemetry_parser.py
    │   ├── web_socket_api/
    │   │   ├── CommandProtocol.py
    │   │   ├── constants.py
    │   │   └── RadioConfiguration.py
    │   ├── web_socket_client/
    │   │   └── WebSocketClient.py
    │   └── spacecomms_interface.py
    └── layer_2/
        └── backend_api.py
```
## File Descriptions
### OBCClientApp.py
DO NOT TOUCH. This is an auto generated script from EnduroSat.

### SerDesHelpers.py
DO NOT TOUCH. This is an auto generated script from EnduroSat.

### realtime_beacon_parser
Used by spacecomms_interface to parse beacons in real time as the are received from spacecomms.

### cobs.py
DO NOT TOUCH. Used by the telemetry parser to do magic cobs stuff.

### datacache.py
DO NOT TOUCH(?). This is an auto generated script from EnduroSat. However, I did have to modify it to handle different sizes for the TaskStats vector, since SSU still has only 30 tasks, while UNH has 36.

### es_crc.py
DO NOT TOUCH. Used for CRC calculations.

### telemetry_parser.py
Parses telemetry data.

### CommandProtocol.py
Probably shouldn't touch this. It is used for sending commands to SpaceComms.

### constants.py
Probably won't need to touch this. It just holds constants used by the spacecomms interface.

### RadioConfiguration.py
Self explanatory. It configures the radio.

### WebSocketClient.py
Used for managing the websocket connection with SpaceComms. Probably shouldn't need to touch this, unless something needs to be changed with the socket configuration.

### spacecomms_interface.py
The main interface for SpaceComms. This lets us send commands to the spacecraft, download files, listen to beacons, etc.

### backend_api.py
The main backend interface. Right now, it takes commands from the terminal, but should eventually be modified to accept web requests from openMCT. Typing a command into the terminal running backend_api.py will route the command to spacecomms_interface.py, which then routes the command to SpaceComms. SpaceComms sends the command over the radio to the spacecraft. The spacecraft generates a response, and sends it back to the groundstation, to be received by SpaceComms. Next, SpaceComms sends the response to spacecomms_interface.py, which does any neccesary parsing, and classifies the response. The response is then put into a queue, which is finally read by backend_api.py.
