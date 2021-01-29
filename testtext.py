#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, line-too-long


import json
import argparse
import urllib.request
from datetime import datetime
import requests
import pytz
from dateutil.tz import tzutc

TZ_UTC = pytz.timezone("UTC")
TZ_LOCAL = pytz.timezone("Europe/Berlin")
UTC_NOW = datetime.now().astimezone(tzutc())

parser = argparse.ArgumentParser(
    description='send test text to display')
parser.add_argument('-d', '--dryrun', default=False, help=r'dry run')
parser.add_argument('-u', '--url', default='http://10.13.37.1/data', help=r'url of textendpoint')
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

MESSAGE = args.text
print(MESSAGE)
PAYLOAD = {'message': MESSAGE, 'intensity': INTENSITY, 'direction': DIRECTION}
if not args.dryrun:
    requests.post(args.url, data=PAYLOAD)
