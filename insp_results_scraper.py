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
                address = str(int(row.findAll('td')[1].contents[0])) + " " + row.findAll('td')[2].contents[0].strip()
                contractor = row.findAll('td')[3].contents[0].strip()
                permit_no = row.findAll('td')[4].contents[0].strip()
                insp_type = row.findAll('td')[5].contents[0].strip()
                result = row.findAll('td')[6].contents[0].strip()
                comment = row.findAll('td')[7].contents[0].strip()
                date = row.findAll('td')[8].contents[0].strip()
                record = {"address": address, "contractor": contractor, "permit_no": permit_no, "insp_type": insp_type, "result": result, "comment": comment, "date": date}
                data.append(record)
            startrow += 50
        except:
            print "Invalid URL"
            break

def export_to_csv(data, ofile):
    f = open("data/" + ofile, 'wt')
    try:
        fieldnames = ('location', 'contractor', 'permit_no', 'insp_type', 'result', 'comment', 'date')
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
        headers = {}
        for r in data:
            location   = r['address'].title()
            contractor = r['contractor'].title()
            permit_no  = r['permit_no']
            insp_type  = r['insp_type'].title()
            result     = r['result']
            comment    = r['comment']
            insp_date  = str(datetime.strptime(r['date'], '%m/%d/%Y'))[:10]

            writer.writerow({'location':location, 'contractor':contractor, 'permit_no':permit_no, \
                             'insp_type':insp_type, 'result':result, 'comment':comment, 'date':insp_date})
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
