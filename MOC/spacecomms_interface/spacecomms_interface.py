from client_apps.OBCClientApp import FP_API_OBC
from web_socket_api.CommandProtocol import send_command
from web_socket_api.constants import SatelliteId, CommandType, TripType, ModuleMac, RadioConfiguration, EncyptionKey
from web_socket_api.RadioConfiguration import set_radio_address, update_frequency, update_aes_key
import logging

# For API containing OBC commands
obc_api = FP_API_OBC()


# Gets uptime from OBC through SpaceComms
def get_uptime():

    # Creating a properly formatted request using the OBC client app API
    serialized_request = list(obc_api.req_getUptime())

    # Sending serialized_request and retrieving response
    serialized_response = send_command(SatelliteId.DEFAULT_ID, CommandType.OBC_FP_GATEWAY, TripType.WAIT_FOR_RESPONSE, ModuleMac.OBC_MAC_ADDRESS, payload=serialized_request)
    
    # Parsing response using OBC client app API
    parsed_response = obc_api.resp_getUptime(serialized_response)

    # Printing s_upTime field of response to console
    logging.info(vars(parsed_response["s__upTime"]))


# Initializing the radio
def init_radio():

    # Setting radio address to the UHF's MAC address
    set_radio_address(ModuleMac.UHF_MAC_ADDRESS)

    # Setting uplink and downlink frequency
    update_frequency(RadioConfiguration.UHF_UPLINK_FREQUENCY, RadioConfiguration.UHF_DOWNLINK_FREQUENCY)

    # Setting the encryption key
    update_aes_key(EncyptionKey.AES_IV, EncyptionKey.AES_KEY)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_radio()

    print("Getting Uptime...")
    get_uptime()
    
