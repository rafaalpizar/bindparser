#!/usr/bin/env python

'''
Tool to parse a bind9 zone conf file to csv


Usage:
cat bind9_zone.conf | python bindconf2csv.py

Author: Rafael Alpizar Lopez

Version: 1.0

Change Log:
2017-12-27 - First version
'''

import pandas as pd
import sys
import re

zones = list()


def process_zones():
    read_zone = True
    lines = sys.stdin.readlines()
    for line in lines:
        #print("Line "+line)
        if line.find('zone') > -1:
            zone = dict()
            try:
                zone['name'] = re.match('zone "(.*)".*', line).group(1)
            except:
                read_zone = False
                print('Line "{}" could not be parsed.'.format(line))
            else:
                read_zone = True
        elif line.find('}', 0, 1) > -1:
            # print(zone)
            zones.append(zone)
            read_zone = False

        if read_zone:
            zone_data = re.match('\s*([\-\w]+)*\s(.*)', line)
            try:
                key = zone_data.group(1)
                value = zone_data.group(2)
                zone[key] = value
            except Exception as e:
                print('Error in line '+line)
                print(e)
                #            print('{}, {}'.format(key, value))

    pd.DataFrame(data=zones).to_excel('/tmp/bindzone.xlsx', sheet_name='Bind Zones')
    return 0


def main():
    test = process_zones()


if __name__ == '__main__':
    main()
