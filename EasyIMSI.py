import pyshark
import requests
import re
import urllib2
from datetime import date
from termcolor import colored


def updatecsv():

    print '\nDownloading up to date MCC/MNC table from http://www.mcc-mnc.com/\n'
    list = open('mcc_mnc_list.txt', 'w')
    td_re = re.compile('<td>([^<]*)</td>' * 6)
    html = urllib2.urlopen('http://mcc-mnc.com/').read()
    table_start = False
    updated = str(date.today())
    list.write(updated + '\n')
    list.write('MCC,MCC (int),MNC,MNC (int),ISO,Country,Country Code,Network')
    for line in html.split('\n'):
        if '<tbody>' in line:
            table_start = True
        elif '</tbody>' in line:
            break
        elif table_start:
            td_search = td_re.search(line)
            csv_line = ''
            for n in range(1, 7):
                group = td_search.group(n).strip().replace(',', '')
                csv_line += group
                if n == 1:
                    csv_line += ',' + str(int(group, 16))
                elif n == 2:
                    if len(group) == 2:
                        mnc_int = int(group + 'f', 16)
                    elif group != 'n/a':
                        mnc_int = int(group, 16)
                    csv_line += ',' + str(mnc_int)
                if n != 6:
                    csv_line += ','
            list.write(csv_line + '\n')
    print '\n --- Download Complete ---\n\n'
    main()


def towerinfo(cell_mcc, cell_mnc, cell_lac, cell_cid):
    url = "https://us1.unwiredlabs.com/v2/process.php"
    payload = "{" \
              "\"token\": \"94c81460a1a00d\"," \
              "\"radio\": \"gsm\"," \
              "\"mcc\": %s," \
              "\"mnc\": %s," \
              "\"cells\": [{\"lac\": %s,\"cid\": %s}]," \
              "\"address\": 1}" \
              % (cell_mcc, cell_mnc, cell_lac, cell_cid)
    response = requests.request("POST", url, data=payload)
    print response.text


def grab_imsi():
    
    capture = pyshark.LiveCapture(interface='lo')
    mcc_mnc_list = open('mcc_mnc_list.txt', 'r').readlines()

    for packet in capture.sniff_continuously():
        if 'Paging Request Type 1' in str(packet):
            try:
                imsi = str(packet[4].e212_imsi)
                mcc = packet[4].e212_mcc
                mnc = str(packet[4].e212_mnc)
                for line in mcc_mnc_list:
                    split = line.split(',')
                    if split[0] == mcc and split[2] == mnc:
                        country = split[5]
                        provider = split[7]
            except:
                continue

            print('imsi: %s | mcc: %s | mnc: %s | country: %s | provider %s') % (imsi, mcc, mnc, country, provider)


def getUserChoice():
    print 'Options:\n'
    try:
        mcclist = open('mcc_mnc_list.txt', 'r')
        updated = mcclist.readline()
        print '1. Update MCC/MNC List - Last updated: %s' % updated
    except:
        print '1. Update MCC/MNC List' + colored(' - No current list found in directory\n', 'red')
    print '2. Scan for IMSIs\n'
    print '3. Retrieve cell tower information. (WIP) \n'
    print 'Type x to exit\n'
    u_in = str(raw_input('$: '))
    if u_in == 'x':
        exit()
    return u_in


def main():
    options = ['1','2','3']
    u_in = '0'
    while u_in not in options:
        if u_in != '0':
            print '\n\n --- Bad Choice! Try Again --- \n\n'
        u_in = getUserChoice()

    if u_in == '1':
        updatecsv()

    elif u_in == '2':
        grab_imsi()

    elif u_in == '3':
        print '\n\n Still WIP \n\n'
        main()
        #towerinfo()

main()
