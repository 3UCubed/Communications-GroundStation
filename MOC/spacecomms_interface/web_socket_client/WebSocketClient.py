import logging
from json import dumps, loads
from traceback import print_exc


class WebSocketClient:
    """Websocket client implementation for GSService interface tests"""

    def __init__(self, enableSSL=True):
        import ssl
        from configparser import ConfigParser

        import websocket

        if enableSSL:

            SERVER_IP = "127.0.0.1"
            SERVER_PORT = "6660"

            # websocket.enableTrace(True)
            URL = "wss://%s:%s" % (SERVER_IP, SERVER_PORT)

            self.connection = websocket.create_connection(
                URL,
                timeout=60,
                sslopt={
                    "check_hostname": False,
                    "ca_certs": "/gs/certificates/CA/rootcert.pem",
                    "certfile": "/gs/certificates/client/clientcert.pem",
                    "keyfile": "/gs/certificates/client/clientkey.pem",
                    "cert_reqs": ssl.CERT_REQUIRED.value,
                },
            )
        # self.connection.settimeout(10.0)
        else:

            URL = "ws://127.0.0.1:6660"
            logging.debug("Attempting connection")
            self.connection = websocket.create_connection(URL, timeout=60)
            logging.debug("Connection established")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            logging.debug("CONNECTION CLOSED")

    def send(self, payload_dict: dict):
        try:
            logging.debug("To Docker: %s", payload_dict)
            self.connection.send(dumps(payload_dict))

        except ConnectionResetError:
            print_exc()
            assert False, "ConnectionResetError"
        except BrokenPipeError:
            print_exc()
            assert False, "BrokenPipeError"

    def readResponse(self):
        try:
            response = self.connection.recv()
            response = loads(response)
            logging.debug("From Docker: %s", response)

        except ConnectionResetError:
            print_exc()
            assert False, "ConnectionResetError"

        return response
