import json
import os
from decouple import config
from core.web3 import Web3Core
from web3 import Web3
from events.models import Transfer
from django.db import transaction, IntegrityError

class CoreContract:
    contract_address_env = None # env variable that holds the target contract address
    contract_abi_file = None # target contract ABI file
    web3 = None # Web3 connection instance

    # Connect to Web3 on every class initialization
    def __init__(self):
        web3core = Web3Core()
        self.web3 = web3core.connect()

    # Method to read a given ABI file.
    # The file is defined by the instance of the class
    # where it is called, via the contract_abi_file variable.
    def get_abi(self):
        # terminate if ABI file is not defined
        if not self.contract_abi_file:
            print("Error: Contract ABI file is not defined")
            return
        
        abi_file = self.contract_abi_file
        with open(abi_file) as f:
            abi = json.load(f)

        return abi["abi"]

    # Method for fetching transfer events based on a given block range.
    # The block limit is set to 'latest' by default if none is specified.
    def get_transfers(self, from_block=None, to_block='latest'):
        # terminate if starting block is not defined
        if not from_block:
            print("Error: Starting block must be specified.")
            return

        # terminate if contract address is not defined
        if self.contract_address_env == None or not config(
            f"{self.contract_address_env}", default=None):
                print("Error: Contract address is not defined.")
                return
        
        # read actual contract address via specified env variable
        contract_address = Web3.to_checksum_address(
            config(self.contract_address_env, default=None))
        
        # initialize contract based on specified contract address and ABI
        contract = self.web3.eth.contract(
            address=contract_address, abi=self.get_abi())

        # fetch transfer events based on specified block range
        events = contract.events.Transfer.create_filter(
            from_block=from_block, to_block=to_block)

        processed_events = [] # list of processed events

        # traverse through the filter result
        # and save each result to the tranfer table in the database
        for event in events.get_all_entries():
            try:
                with transaction.atomic(): # atomic wrapper to rollback on exception
                    Transfer.objects.create(
                        token_id=event.get('args').get('tokenId'),
                        sender=event.get('args').get('from'),
                        recipient=event.get('args').get('to'),
                        trn_hash=event.get('transactionHash').hex(),
                        block_no=event.get('blockNumber')
                    )
                print(f"Transfer event for token {event.get('args').get('tokenId')} with transaction hash {event.get('transactionHash').hex()} has been recorded successfully.")
            except IntegrityError:
                print(f"Transfer event for token {event.get('args').get('tokenId')} with transaction hash {event.get('transactionHash').hex()} already exists. Event skipped.")
