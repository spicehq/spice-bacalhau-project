import pickle
import sys
import subprocess

def get_cid(path):
    if "/" in path:
        print(f"resolving the CID {path}", file=sys.stderr)
        cid = subprocess.check_output(['ipfs', 'resolve', path]).decode().splitlines()[0][6:]
        return cid

    return path

def generate_volume_args(uris):
    volumes = []
    cidMap = {}
    for i, uri in enumerate(uris):
        if not uri.startswith("ipfs://"):
            continue

        path = uri.replace("ipfs://", "")
        try:
            cid = get_cid(path)
            if cid in cidMap:
                print(f"skipping duplicate CID: {cid}", file=sys.stderr)
                continue
            cidMap[cid] = True
            volumes.append(f"-v {cid}:/inputs/{i}")
        except:
            pass
    
    return " ".join(volumes)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate volume arguments to mount ipfs uris as inputs to bacalhau job')
    parser.add_argument('uri_file', type=str)
    parser.add_argument('--max-uris', default=50, type=str)

    args = parser.parse_args()

    with open(args.uri_file, "rb") as f:
        uris = pickle.load(f)
    print(generate_volume_args(uris[:args.max_uris]))
