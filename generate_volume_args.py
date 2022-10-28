import pickle
import requests


def get_cid(path):
    if "/" in path:
        cid, name = tuple(path.split("/"))
        dag = requests.get(f"https://ipfs.io/api/v0/dag/get?arg={cid}").json()
        cid = [link["Hash"]["/"] for link in dag["Links"] if link["Name"] == name]
        if cid:
            return cid[0]
        raise RuntimeError()

    return path


def generate_volume_args(uris):
    volumes = []
    for i, uri in enumerate(uris):
        if not uri.startswith("ipfs://"):
            continue

        path = uri.replace("ipfs://", "")
        try:
            cid = get_cid(path)
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
