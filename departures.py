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
    description='receive departure data from marudor and post ist to a web interface')
parser.add_argument(
    '-a', '--api', default='https://marudor.de/api/hafas/v2/departureStationBoard/?station=', help=r'api endpoint url')
parser.add_argument('-s', '--station', default='008004965', help=r'station id')
parser.add_argument('-c', '--amount', default=3, help=r'max amount of departures to show')
parser.add_argument('-d', '--dryrun', default=False, help=r'dry run')
parser.add_argument('-u', '--url', default='http://10.13.37.1/data', help=r'url of textendpoint')
parser.add_argument('-m', '--min', default=0, help=r'minimum minutes to departure')
parser.add_argument('-n', '--max', default=90, help=r'max minutes to departure')
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
        r_data = open_url.read()
        json_data = json.loads(r_data)
    else:
        print("Error receiving DATA", open_url.getcode())
    return json_data

DATA = get_response(args.api + args.station)

MESSAGE = ""
COUNT_MESSAGE = 0
for dep in DATA:
    if COUNT_MESSAGE + 1 > int(args.amount):
        break
    dt_obj_dep = TZ_UTC.localize(datetime.strptime(dep['departure']['time'], '%Y-%m-%dT%H:%M:%S.%fZ'))
    dt_obj_sch = TZ_UTC.localize(datetime.strptime(dep['departure']['scheduledTime'], '%Y-%m-%dT%H:%M:%S.%fZ'))
    diff_m_dep = round((dt_obj_dep - UTC_NOW).total_seconds() / 60)
    diff_m_sch = round((dt_obj_sch - UTC_NOW).total_seconds() / 60)
    dest = dep['finalDestination'].split(',')[0]
    dest = dest.split(' ')[0]
    dest = dest.replace('ß', 'ss')
    dest = dest.replace('strasse', 'str.')
    if diff_m_dep < int(args.max) and diff_m_dep > int(args.min):
        if len(MESSAGE) > 0:
            MESSAGE += " / "
        if diff_m_sch < diff_m_dep:
            MESSAGE += str(diff_m_dep) + 'min: ' + dest + ' (+' + str(diff_m_dep-diff_m_sch)+ ')'
            COUNT_MESSAGE += 1
        else:
            MESSAGE += str(diff_m_dep) + 'min: ' + dest
            COUNT_MESSAGE += 1

if COUNT_MESSAGE == 0:
    MESSAGE = TZ_LOCAL.localize(datetime.now()).strftime('%H:%M')

print(MESSAGE)
PAYLOAD = {'message': MESSAGE, 'intensity': INTENSITY, 'direction': DIRECTION}
if not args.dryrun:
    requests.post(args.url, data=PAYLOAD)
