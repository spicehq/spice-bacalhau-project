# Demo scripts for generating an NFT collage using Bacalhau

## Overview

The general process to generate the collage is

- Get a list of ipfs uris from the target contract 
- Run a bacalhau job to get image links from the metadata files
- Run a bacalhau job to generate the collage from the image files 

## Notes:
`script.py` should be added to IPFS so it can be run in the bacalhau job (`ipfs add script.py`). The resulting CID can then be mounted in the container and run

Currently there's a `good_uris.pkl` containing a list of ipfs uris from vitalik.eth's wallet. The `good_tokens.pkl` contains a list of (token_address, token_id) tuples that are tokens that have metadata on IPFS. This list could be used to filter tokens before calling the `tokenUri` method in real time

The `generate_volume_args` script/function can be used to generate a string with multiple `-v IPFS_CID:filename` arguments that can be added to the bacalhau job. This function also uses the public ipfs gateway to get file cids when the URI found on chain or in metadata is of the form `DIRECTORY_CID/filename`. This allows the individual file to be mounted to the job instead of the whole ipfs directory (slow)

This script can be used directly when triggering the bacalhau job like
`bacalhau docker run $(python3 yakoa/bacalhau-test/scripts/gen_command.py ~/good_uris.pkl) -v QmRwNmAo1t9VMK6ww1DMPzQiP3xGiKSVnASEDsAnbZ6dhT:/script.py jonahyakoa/bacalhau-demo -- python /script.py parse_metadata`
