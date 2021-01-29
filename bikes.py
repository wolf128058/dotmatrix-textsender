#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, line-too-long

import argparse
import json
import urllib.request
import requests

parser = argparse.ArgumentParser(
    description='send test text to display')
parser.add_argument('-d', '--dryrun', default=False, help=r'dry run')
parser.add_argument('-u', '--url', default='http://10.13.37.1/data', help=r'url of textendpoint')
parser.add_argument('-s', '--station', default='23328', help=r'station id')
parser.add_argument('-t', '--text', default='The quick brown fox jumps over the lazy dog', help=r'max minutes to departure')
parser.add_argument('-i', '--intensity', default=10, help=r'intensity 0-15')
parser.add_argument('-r', '--direction', default=0, help=r'direction')

args = parser.parse_args()

INTENSITY = int(args.intensity)
if INTENSITY < 0 or INTENSITY > 15:
    INTENSITY = 10

DIRECTION = int(args.direction)
if DIRECTION < 0 or DIRECTION > 2:
    DIRECTION = 0

def get_response(url):
    open_url = urllib.request.urlopen(url)
    if open_url.getcode() == 200:
        data = open_url.read()
        json_data = json.loads(data)
    else:
        print("Error receiving data", open_url.getcode())
        return None
    return json_data

station_data = get_response('https://mobil.tws.de/mbroker/rest/areainformation/' + args.station)
print(station_data['sharingAvailability']['availableVehicles'])

payload = {'message': str(station_data['sharingAvailability']['availableVehicles']) + ' Bikes available'}

if not args.dryrun:
    requests.post(args.url, data=payload)
