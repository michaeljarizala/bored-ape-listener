from web3 import Web3
from decouple import config


class Web3Core:
    # Method for establishing connection to Web3.
    # The RPC URL is defined via the INFURA_URL_ETH_MAINNET env variable.
    # This function can be further enhanced to behave more flexibly
    # in which the user can have the option to dynamically choose the
    # RPC URL to use, e.g. Sepolia test network.
    #
    # But since we are focusing on BAYC for now which is on the Ethereum mainnet,
    # the current implementation should suffice.
    def connect(self):
        web3 = None

        web3 = Web3(Web3.HTTPProvider(config(
            "INFURA_URL_ETH_MAINNET", default=None)))

        if web3 and web3.is_connected():
            print("Web3 connection established!")
            return web3
        
        raise OperationalError("Could not established connection to Web3.")