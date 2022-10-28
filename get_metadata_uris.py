import pickle
# Todo load spice tokens and make calls to tokenUri
# Can either make rpc calls live or cache results
# The pickle `good_tokens` can be used to filter vitalik.eth's tokens for only ipfs nfts (metadata)
uris = []

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


uris = [clean_uri(uri) for uri in uris if clean_uri(uri)]

# Write uris to a pickle that can be loaded by `generate_volume_args.py`.
# Could also pass the list directly to generate_volume_args(...)
with open("metadata_uris.pkl", "wb") as f:
    pickle.dump(uris, f)    

