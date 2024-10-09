import argparse
import django
import os

# Set the settings module for your Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bored-ape-listener.settings')
django.setup()

from core.contracts import CoreContract

def main(args):
    contract = CoreContract()
    contract.contract_abi_file = "core/abis/TransferABI.json"
    contract.contract_address_env = "BAYC_CONTRACT_ADDRESS"
    contract.get_transfers(from_block=args.start, to_block=args.end if args.end else 'latest')

if __name__ == "__main__":

    cmd = argparse.ArgumentParser(description="Fetch transfer events and persist filter result to database.")
    cmd.add_argument("--start", type=int, required=True, help="Start of events range to listen to.")
    cmd.add_argument("--end", type=int, required=False, help="End of events range to listen to. Defaults to 'latest' if not specified.")

    cmd_args = cmd.parse_args()

    main(cmd_args)