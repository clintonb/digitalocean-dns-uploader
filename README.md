# digitalocean-dns-uploader
This script can be used to load a DNS zone file into DigitalOcean.

NOTE: Due to a limitation of the `blockstack-zones` dependency, only Python 2.7 is supported. See
https://github.com/blockstack/zone-file-py/pull/5.


## Getting Started

1. Obtain your API key/token if you haven't already. See ttps://www.digitalocean.com/help/api/.

2. Install the requirements.

        pip install -r requirements.txt

3. Run the script.

        DO_API_TOKEN=<api-key> ./upload_zone_file.py <file-path>


## Migrating from AWS

I originally wrote this script to migrate zones from AWS Route53 to Digital Ocean. AWS does not support exporting zone
files. However, the [cli53](https://github.com/barnybug/cli53) command line tool can export BIND zone files.


## Known Limitations

1. MX, NS, and SOA records are ignored.

    - Personally, I use Gmail's servers and the DigitalOcean user interface offers a
button to install those.
    - NS records are already defined.
    - The DigitalOcean API does not support editing SOA records. See https://digitalocean.uservoice.com/forums/136585-digitalocean/suggestions/3655172-configurable-soa-record-in-dns.

2. The script only creates new records. It does not know how to update existing records.

    - Attempts to create a duplicate CNAME record will fail.
    - Attempts to create duplicate records of other types will most likely **create duplicate records**.

3. ME! I'm hacking on this at 2:30 AM. Expect little, if any, support.
