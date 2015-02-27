#!/usr/bin/env python
"""Scraper for City of Chesapeake Inspection Results"""

import sys
import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime, date


def scraper(data):
    """We are getting the inspection statuss data from the City of
       Chesapeake's inspection statuss website using BeautifulSoup. Each <td>
       in the <tr> is saved in a python dictionary. Each <tr> is saved in
       an array."""
    startrow = 1
    while startrow < 1500:
        url = get_url(startrow)
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text)

            t = soup.findAll('table')[1]
            rows = t.findAll('tr')[1:]
            for row in rows:
                status_id = row.findAll('td')[0].contents[0]
                location = str(int(row.findAll('td')[1].contents[0])) + " " \
                  + row.findAll('td')[2].contents[0].strip()
                contractor = row.findAll('td')[3].contents[0].strip()
                permit_number = row.findAll('td')[4].contents[0].strip()
                inspection_type = row.findAll('td')[5].contents[0].strip()
                status = row.findAll('td')[6].contents[0].strip()
                comments = row.findAll('td')[7].contents[0].strip()
                inspection_date = row.findAll('td')[8].contents[0].strip()

                record = {"location": location,
                          "contractor": contractor,
                          "permit_number": permit_number,
                          "inspection_type": inspection_type,
                          "status": status,
                          "comments": comments,
                          "inspection_date": inspection_date}

                data.append(record)

            startrow += 50
        except:
            print("Invalid URL")
            break


def export_to_json(data, jsonfile):
    try:
        f = open("data/" + jsonfile, 'wt')
        json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))
    finally:
        f.close()


def export_to_csv(data, csvfile):
    f = open("data/" + csvfile, 'wt')
    try:
        fieldnames = ('location',
                      'contractor',
                      'permit_number',
                      'inspection_type',
                      'status',
                      'comments',
                      'inspection_date')

        #headers = {}

        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')

        #for n in writer.fieldnames:
        #    headers[n] = n
        #writer.writerow(headers)

        for row in data:
            location = row['location'].upper()
            contractor = row['contractor'].upper()
            permit_number = row['permit_number']
            inspection_type = row['inspection_type'].upper()
            status = row['status']
            comments = row['comments']
            inspection_date = str(datetime.strptime(row['inspection_date'],
                                  '%m/%d/%Y'))[:10]

            writer.writerow({'location': location,
                             'contractor': contractor,
                             'permit_number': permit_number,
                             'inspection_type': inspection_type,
                             'status': status,
                             'comments': comments,
                             'inspection_date': inspection_date})
    finally:
        f.close()


def get_url(startrow):
    return 'http://ez.cityofchesapeake.net/cfusion/inspections/inspresult_permitsort.cfm?startrow=%s' % startrow


def main():
    today = date.today()
    csvfile = "chesapeake_inspection_results_" + str(today.year) + "-" + \
        str(today.month) + "-" + str(today.day) + ".csv"
    jsonfile = "chesapeake_inspection_results_" + str(today.year) + "-" + \
        str(today.month) + "-" + str(today.day) + ".json"
    data = []
    scraper(data)
    export_to_csv(data, csvfile)
    export_to_json(data, jsonfile)

    if len(data) > 0:
        print("There are %d inspection results today." % len(data))

if __name__ == '__main__':
    main()
