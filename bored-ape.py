import argparse
import django
import os

# Set the settings module for your Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bored-ape-listener.settings')
django.setup()

from core.contracts import CoreContract

def main():
    contract = CoreContract()
    contract.contract_abi_file = "core/abis/TransferABI.json"
    contract.contract_address_env = "BAYC_CONTRACT_ADDRESS"
    contract.get_transfers(from_block=20925802)

if __name__ == "__main__":
    
    main()