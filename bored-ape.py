import argparse
import django
import os
from core.web3 import Web3Core

# Set the settings module for your Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bored-ape-listener.settings')
django.setup()

def main():
    web3 = Web3Core()
    web3.connect()

if __name__ == "__main__":

    main()