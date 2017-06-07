#!/usr/bin/env python
import json
import logging
import os
import sys

import requests
from blockstack_zones import parse_zone_file

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)

API_TOKEN = os.environ['DO_API_TOKEN']


def create_domain_record(domain, **kwargs):
    headers = {
        'Authorization': 'Bearer ' + API_TOKEN,
        'Content-Type': 'application/json',
    }
    endpoint = 'https://api.digitalocean.com/v2/domains/{}/records'.format(domain)
    response = requests.post(endpoint, data=json.dumps(kwargs), headers=headers)
    if response.ok:
        log.info('Created new %s record %s.', kwargs['type'], kwargs['name'])
    else:
        error_message = response.json()['message']
        log.error('Failed to create %s record %s. Error was: %s', kwargs['type'], kwargs['name'], error_message)


def main(argv):
    domain_name, zone_file = _parse_zone_file(argv[0])
    for record_type, records in zone_file.items():
        record_type = record_type.upper()

        # NOTE: I default to the Gmail option in the UI.
        # NS and SOA records should be provided by DigitalOcean.
        if record_type not in ('MX', 'NS', 'SOA'):
            for record in records:
                if record_type == 'CNAME':
                    record['data'] = record['alias'] + '.'
                elif record_type == 'TXT':
                    record['data'] = record['txt']
                elif record_type == 'A':
                    record['data'] = record['ip']

                create_domain_record(
                    domain_name,
                    type=record_type,
                    name=record['name'],
                    ttl=record['ttl'],
                    data=record['data']
                )


def _parse_zone_file(path):
    """
    Parse the zone file.

    Args:
        path (str): Path to the zone file

    Returns:
        str: Domain name
        dict[]: Domain records
    """
    log.info('Parsing %s...', path)

    with open(path, 'r') as f:
        zone_file = parse_zone_file(f.read())

    domain_name = zone_file.pop('$origin').strip('.')
    record_count = sum([len(records) for records in zone_file.itervalues()])
    log.info('Parsed %d records for %s.', record_count, domain_name)

    return domain_name, zone_file


if __name__ == '__main__':
    main(sys.argv[1:])
