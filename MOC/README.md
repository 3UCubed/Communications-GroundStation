# Description
Multiple scripts that can be used to parse beacons, communicate with the SpaceComms terminal, and parse telemetry files.

# Quick-Start
Ensure SpaceComms is running

Open a terminal in your documents directory, or wherever you keep your git repos

Clone the repository: ```git clone https://github.com/3UCubed/Communications-GroundStation.git```

Change directory into the repo: ```cd Communications-GroundStation/```

## I want to... Download all telemetry files from the OBC
Change directory into spacecomms_interface: ```cd MOC/spacecomms_interface/```

Start downloading all .TLM files: ```python3 spacecomms_interface.py 2```

## I want to... Parse all of the telemetry files I downloaded
Copy all .TLM files from MOC/spacecomms_interface/downloaded_files

Paste all .TLM files you want to parse into MOC/telemetry_parser/tlm_files

Change directory into telemetry_parser: ```cd MOC/telemetry_parser/```

Start parsing your .TLM files: ```python3 telemetry_parser.py```

## I want to... Parse beacon data in real-time
Change directory into realtime_beacon_parser: ```cd MOC/beacon_parser/realtime_beacon_parser/```

Start listening for beacons and parsing: ```python3 realtime_beacon_parser.py```


# Directory Structure
```
MOC/
├─ spacecomms_interface/
│  ├─ client_apps/
│  │  ├─ OBCClientApp.py
│  │  ├─ SerDesHelpers.py
│  ├─ downloaded_files/
│  ├─ raw_beacons/
│  ├─ web_socket_api/
│  │  ├─ CommandProtocol.py
│  │  ├─ constants.py
│  │  ├─ RadioConfiguration.py
│  ├─ web_socket_client/
│  │  ├─ __init__.py
│  │  ├─ WebSocketClient.py
│  ├─ spacecomms_interface.py
├─ telemetry_parser/
│  ├─ csv_files/
│  ├─ dependencies/
│  │  ├─ cobs.py
│  │  ├─ datacache.py
│  │  ├─ es_crc.py
│  ├─ tlm_files/
│  ├─ SerDesHelpers.py
│  ├─ telemetry_parser.py
├─ beacon_parser/
│  ├─ beacon_file_parser/
│  │  ├─ beacon_file_parser.py
│  │  ├─ raw_beacon.bin
│  ├─ realtime_beacon_parser/
│  │  ├─ realtime_beacon_parser.py
```

## spacecomms_interface
### Description
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Used for interfacing with the SpaceComms terminal.

#### client_apps/ 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains scripts used for helping deserialize radio responses. Do not touch.

#### downloaded_files/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;All files downloaded are placed here.

#### raw_beacons/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Currently unused. Was previously used for storing a binary file containing raw beacons.

#### web_socket_api/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Command Protocol.py: Implementation of send_command. Do not touch.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;constants.py: Constants used throughout the SpaceComms interface. Do not touch.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RadioConfiguration.py: Implementation of various radio setup functions. Contains start_beacon_listening implementation.

#### web_socket_client/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Honestly, I don't think the scripts in here are even used. Do not touch.

#### spacecomms_interface.py
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Main script used to interface with SpaceComms.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__Usage__: ```python3 spacecomms_interface.py <num>```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Where num is either 1, 2, or 3. 1 gets uptime, 2 starts downloading all telemetry files, and 3 starts beacon listening.


## telemetry_parser
### Description
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Used for parsing .TLM files.

#### csv_files/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;All generated csv files are placed here. For each .TLM file parsed, a new directory will be 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;created with the name of the parsed .TLM file. For instance, if '00017.TLM' is parsed, 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a new directory named '00017' will be created, and a CSV for each subsystem will be generated and placed here.

#### dependencies/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains helper scripts for telemetry parsing. Do not touch.

#### tlm_files/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Place all .TLM files that you want parsed in this directory. The telemetry parser will look through
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;this entire directory and parse every .TLM file placed here.

#### SerDesHelpers.py
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Helper script for deserializing data. Do not touch.

#### telemetry_parser.py
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Main script used to parse all .TLM files located in the /tlm_files/ directory.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__Usage__: ```python3 telemetry_parser.py```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Running this command will start the process of parsing all .TLM files the user placed in the /tlm_files/ directory.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Individual CSV files are generated from the parsed data, and are located in the /csv_files/ directory.


## beacon_parser/
### Description
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains two seperate projects: one for parsing .bin files containing beacons, and one for parsing beacons in real time.

#### beacon_file_parser/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains a script to parse raw beacon data contained in raw_beacons.bin.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__Usage__: ```python3 beacon_file_parser.py```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Running this script will print the parsed beacons in the terminal.


#### realtime_beacon_parser/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains a script to parse beacons in real-time. It works by _internally_ executing ```python3 spacecomms.py 3```, which

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;starts the beacon listener implemented in spacecomms.py. The realtime_beacon_parser.py script pipes the output of the 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;spacecomms.py script to itself, which gives it real-time access to the received beacons. Upon receiving a beacon, the

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;realtime_beacon_parser.py script parses it, and prints the parsed beacon to the console.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__Usage__: ```python3 realtime_beacon_parser.py```
