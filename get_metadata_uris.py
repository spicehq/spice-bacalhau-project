import pickle
import csv
from web3 import Web3
import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_uris(csv_file):
    WEB3_PROVIDER_URL=os.getenv("WEB3_PROVIDER_URL")
    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

    erc721_abi = {}
    with open("abi/erc721.json", "r") as erc721_abi_f:
        erc721_abi = json.loads(erc721_abi_f.read())

    uris = []
    with open(csv_file, "r") as f:
        nft_owners_reader = csv.reader(f)
        next(nft_owners_reader) # remove the headers
        for p in nft_owners_reader:
            token_contract = w3.eth.contract(Web3.toChecksumAddress(p[0].lower()), abi=erc721_abi)
            try:
                uri = token_contract.functions.tokenURI(int(p[1])).call()
            except:
                continue
            print(uri)
            uris.append(uri)
    
    return [clean_uri(uri) for uri in uris if clean_uri(uri)]

def clean_uri(uri):
    if uri.startswith("https://ipfs.io/ipfs/"):
        uri = uri.replace("https://ipfs.io/ipfs/", "ipfs://")
    if uri.startswith("ipfs://"):
        # Do nothing
        pass
    else:
        # Not a parsable ipfs uri, return None
        return None
    return uri


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Get IPFS metadata files to pass to bacalhau')
    parser.add_argument('results_file', type=str)

    args = parser.parse_args()

    uris = get_uris(args.results_file)

    # Write uris to a pickle that can be loaded by `generate_volume_args.py`.
    # Could also pass the list directly to generate_volume_args(...)
    with open("metadata_uris.pkl", "wb") as f:
        pickle.dump(uris, f)    
