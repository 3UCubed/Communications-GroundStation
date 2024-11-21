
class SatelliteId():
   DEFAULT_ID = "2"

class CommandType():
    UHF_FP_GATEWAY = 1300
    SBAND_FP_GATEWAY = 1300
    OBC_FP_GATEWAY = 1212
    OBC_FILE_DOWNLOAD = 1450
    EPS_FP_GATEWAY = 1212

class TripType():
    WAIT_FOR_RESPONSE = 1
    NO_WAIT_FOR_RESPONSE = 0

class ModuleMac():
    UHF_MAC_ADDRESS = 0x11
    SBAND_MAC_ADDRESS = 0x44
    SBAND_2_MAC_ADDRESS = 0x45
    OBC_MAC_ADDRESS = 0x33
    PDM_MAC_ADDRESS = 0x77
    BP_1_MAC_ADDRESS = 0x66
    BP_2_MAC_ADDRESS = 0x67
    BP_3_MAC_ADDRESS = 0x68

class EncyptionKey():
    AES_IV = "AAECAwQFBgcICQoLDA0ODw=="
    AES_KEY = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
    # Note: The following is the hex version of the key the line above (which is base64 encoded)
    # "6983271bf7dd48a65f3acec433cad925a432bc3227f87734d9d76aab2b68b6f1"
    # This is what is fed into SpacePY UHF WriteCipherSlot
    # With a new 32 byte key, you can translate it into the base64 version and put it in this file
    # UNH has a python script that generates a series of keys, although it is overkill for how much is needed

class RadioConfiguration():
    SBAND_UPLINK_FREQUENCY = 2102500000
    SBAND_DOWNLINK_FREQUENCY = 2277500000
    UHF_UPLINK_FREQUENCY = 435000000
    UHF_DOWNLINK_FREQUENCY = 436500000