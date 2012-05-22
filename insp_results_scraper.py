import sys, os
import urllib, urllib2
from bs4 import BeautifulSoup
import csv
from datetime import datetime, date

def scraper(data):
    """We are getting the inspection results data from the City of 
       Chesapeake's inspection results website using BeautifulSoup. Each <td> 
       in the <tr> is saved in a python dictionary. Each <tr> is saved in 
       an array."""
       
    startrow = 1
    while startrow < 1500:
        url = get_url(startrow)
        try:
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html)

            t = soup.findAll('table')[1]
            rows = t.findAll('tr')[1:]
            for row in rows:
                result_id = row.findAll('td')[0].contents[0]
                location = str(int(row.findAll('td')[1].contents[0])) + " " + \
                                   row.findAll('td')[2].contents[0].strip()
                contractor = row.findAll('td')[3].contents[0].strip()
                permit_number = row.findAll('td')[4].contents[0].strip()
                inspection_type = row.findAll('td')[5].contents[0].strip()
                result = row.findAll('td')[6].contents[0].strip()
                comments = row.findAll('td')[7].contents[0].strip()
                inspection_date = row.findAll('td')[8].contents[0].strip()

                record = {"location": location, 
                          "contractor": contractor, 
                          "permit_number": permit_number, 
                          "inspection_type": inspection_type, 
                          "result": result, 
                          "comments": comments, 
                          "inspection_date": inspection_date}

                data.append(record)

            startrow += 50
        except:
            print "Invalid URL"
            break

def export_to_csv(data, ofile):
    f = open("data/" + ofile, 'wt')
    try:
        fieldnames = ('location',
                      'contractor',
                      'permit_number',
                      'inspection_type',
                      'result',
                      'comments',
                      'inspection_date')

        headers = {"location",
                   "contractor",
                   "permit_number",
                   "inspection_type",
                   "result",
                   "comments",
                   "inspection_date"}

        writer = csv.DictWriter(f, headers=headers, fieldnames=fieldnames, delimiter='|')

        for r in data:
            location         = r['location'].title()
            contractor       = r['contractor'].title()
            permit_number    = r['permit_number']
            inspection_type  = r['inspection_type'].title()
            result           = r['result']
            comments         = r['comments']
            inspection_date  = str(datetime.strptime(r['inspection_date'], \
                                                     '%m/%d/%Y'))[:10]

            writer.writerow({'location':location,
                             'contractor':contractor,
                             'permit_number':permit_number,
                             'inspection_type':inspection_type,
                             'result':result,
                             'comments':comments,
                             'inspection_date':inspection_date})
    finally:
        f.close()

def get_url(startrow):
    return 'http://ez.cityofchesapeake.net/cfusion/inspections/inspResult_permitsort.cfm?startrow=%s' % startrow

def main():
    today = date.today()
    ofile = "chesapeake_inspection_results_" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
    data = []
    scraper(data)
    export_to_csv(data, ofile)

    if len(data) > 0:
        print "There are %d inspection results today." % len(data)

if __name__ == '__main__':
    main()
