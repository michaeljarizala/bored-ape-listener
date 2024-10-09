import json
import os
from decouple import config
from core.web3 import Web3Core
from web3 import Web3
from events.models import Transfer
from django.db import transaction, IntegrityError

class CoreContract:
    contract_address_env = None
    contract_abi_file = None
    web3 = None

    def __init__(self):
        web3core = Web3Core()
        self.web3 = web3core.connect()

    def get_abi(self):
        if not self.contract_abi_file:
            print("Error: Contract ABI file is not defined")
            return
        
        base_dir = os.path.dirname(__file__)
        abi_file = self.contract_abi_file
        with open(abi_file) as f:
            abi = json.load(f)

        return abi["abi"]

    def get_transfers(self, from_block=None, to_block='latest'):
        if not from_block:
            print("Error: Starting block must be specified.")
            return

        if self.contract_address_env == None or not config(f"{self.contract_address_env}", default=None):
            print("Error: Contract address is not defined.")
            return
        
        contract_address = Web3.to_checksum_address(
            config(self.contract_address_env, default=None))
        contract = self.web3.eth.contract(address=contract_address, abi=self.get_abi())

        events = contract.events.Transfer.create_filter(from_block=from_block, to_block=to_block)

        processed_events = []

        for event in events.get_all_entries():
            try:
                processed_events.append({
                    "token_id": event.get('args').get('tokenId'),
                    "sender": event.get('args').get('from'),
                    "recipient": event.get('args').get('to'),
                    "trn_hash": event.get('transactionHash').hex(),
                    "block_no": event.get('blockNumber'),
                })
                
                print(f"Transfer event for token {event.get('args').get('tokenId')} with transaction hash {event.get('transactionHash').hex()} has been recorded successfully.")
            except IntegrityError:
                print(f"Transfer event for token {event.get('args').get('tokenId')} with transaction hash {event.get('transactionHash').hex()} already exists. Event skipped.")
        
        return processed_events
