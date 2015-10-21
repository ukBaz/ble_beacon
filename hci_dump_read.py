#!/usr/bin/python
"""
Example line from hcidump.
> 04 3E 21 02 01 00 00 E3 E3 03 5B 02 00 15 02 01 1A 03 03 D8
  FE 0D 16 D8 FE 00 14 02 63 73 72 2E 63 6F 6D A7
  
Looking at:
https://github.com/AltBeacon/spec
And more importantly:
https://github.com/google/uribeacon/blob/master/specification/AdvertisingMode.md

The data can be broken up as follows:
preamble: 04
Access Address: 3E 21 02 01
PDU Header: 00 00
Adv Address: E3 E3 03 5B 02 00
Ad Flags: 15 02 01
???: 1A (Decimal 26)
Ad Length: 03
Ad Type (Service UUID's): 03
Service UUID: FE D8
Ad Lenght: 0D (decimal 13)
Ad Type (Service data): 16
Service UUID: FE D8
Flags: 00
Calibrated Tx Power: 14 (decimal 20)
Uri Scheme Prefix: 02 (maps to 'http://')
Encoded Uri: 63 73 72 2E 63 6F 6D (csr.com)
RSSI: A7 (deciaml -89)

"""

import re
import subprocess
import math
import os

import numpy as np


def mac_address(bytes):
    # bytes[13] ":" bytes[12] ":" bytes[11] ":" bytes[10] ":" bytes[9] ":" bytes[8]
    address = '{0}:{1}:{2}:{3}:{4}:{5}'.format(bytes[12], bytes[11],
                            bytes[10], bytes[9], bytes[8], bytes[7])
    return address

def packet_len(data, loc):
    return int(data[loc], 16)
    
def service(data):
    # Complete List of 16-Dit Service
    pass

def service_id(data):
    # Assigned Uri Service UUID
    # 0xFED8
    pass

def ad_length(data, loc):
    # Between 5 - 23
    return int(data[loc], 16)

def service_data(data):
    # 0x16
    pass

def service_id2(data):
    # Assigned Uri Service UUID
    # This one in ad content
    # 0xFED8
    pass

def uri_flags(data):
    # UriBeacons Flags
    pass

def tx_power(data, loc):
    # Reference power from beacon broadcast
    tx_power = int(data[loc + 5], 16)
    if tx_power & 0x80: # MSB set -> neg.
        return -((~tx_power & 0xff) + 1)
    else:
        return tx_power

def uri_scheme(data, loc):
    # Get UriBeacon Uri Scheme Prefix
    # 0x00 = http://www.
    # 0x01 = https://www.
    # 0x02 = http://
    # 0x03 = https://
    # 0x04 = urn:uuid:
    encode_scheme = {0: 'http://www.',
                     1: 'https://www.',
                     2: 'http://',
                     3: 'https://',
                     4: 'urn:uuid:'}
    return encode_scheme[int(data[loc + 6])]

def url_encoding(code):
    # UriBeacon HTTP URL encoding
    # 0	0x00	.com/
    # 1	0x01	.org/
    # 2	0x02	.edu/
    # 3	0x03	.net/
    # 4	0x04	.info/
    # 5	0x05	.biz/
    # 6	0x06	.gov/
    # 7	0x07	.com
    # 8	0x08	.org
    # 9	0x09	.edu
    # 10	0x0a	.net
    # 11	0x0b	.info
    # 12	0x0c	.biz
    # 13	0x0d	.gov
    encode_scheme = {0: '.com/',
                     1: '.org/',
                     2: '.edu/',
                     3: '.net/',
                     4: '.info/',
                     5: '.biz/',
                     6: '.gov/',
                     7: '.com',
                     8: '.org',
                     9: '.edu',
                     10: '.net',
                     11: '.info',
                     12: '.biz',
                     13: '.gov'}
    return encode_scheme[int(code)]

def encoded_uri(data, loc, length):
    start = loc + 7
    # Uri content
    val = ''
    for i in data[start:(start + length - 6)]:
        # print 'Encode: {0} - {1}'.format(i, chr(int(i, 16)))
        if int(i, 16) < 14:
            val = val + url_encoding(i)
        else:
            val = val + chr(int(i, 16))
    return val
        

def rssi_value(data):
    # Get recieve signal strength
    rssi = int(data[-1], 16)
    if rssi & 0x80: # MSB set -> neg.
        return -((~rssi & 0xff) + 1)
    else:
        return rssi

def has_uribeacon_service(data):
    return (data[14] == '03' and
            data[15] == '03' and
            data[16] == 'D8' and
            data[17] == 'FE')

def find_ad_start(data):
    uri_service = ['03', '03', 'D8', 'FE']
    service_loc = [(i, i+len(uri_service)) for i in range(len(data)) if data[i:i+len(uri_service)] == uri_service]
    return service_loc
 

def calc_range(rssi, txpower):
    # Alternative calculation to test, likely very similar answer!
    # rssi1m needs to be found with testing
    # Based on; http://matts-soup.blogspot.co.uk/2013/12/finding-distance-from-rssi.html

    #  Using zero for rssi1m as currently beacons are broadcasting value a 1m via txPower
    rssi1m = -40 #  tested
    path_loss = 2 #  free space
    if rssi > 0:
        rssi = 0
    act_power = txpower + rssi1m
    pwr_loss = rssi - act_power
    num = -10 * path_loss
    den = float(pwr_loss) / float(num)
    raw_range = math.pow(10.0, den)
    return raw_range

def process_line(complete_line):
    mydata = complete_line.split()

    if len(mydata) > 0:
        if mydata[0] == '>':
            del mydata[0]
            # print mydata[14]

        if len(find_ad_start(mydata)) > 0:
            data_start = find_ad_start(mydata)[0][1]
            # print mydata[-1]
            print '  Address: {}'.format(mac_address(mydata))
            print '  uri: {}{}'.format(uri_scheme(mydata, data_start),
                                       encoded_uri(mydata, data_start, ad_length(mydata, data_start)))
            print '  TX power: {}'.format(tx_power(mydata, data_start))
            print '  RSSI: {}'.format(rssi_value(mydata))
            print '  distance: {}'.format(calc_range(rssi_value(mydata),
                                                        tx_power(mydata, data_start)))
            print '  Length: {}'.format(ad_length(mydata, data_start))
            # fo.write( '{0},'.format(rssi_value(mydata)))
            print '\n'


def main():
   gotOK = 0
   # Open a file
   # fo = open("logging.txt", "wb")
   file_path = os.path.dirname(os.path.realpath(__file__))
   cmd = os.path.join(file_path, 'hcidump.sh')
   print cmd
   reader = subprocess.Popen(cmd, 
                           shell=False,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           )

   line = '' 
   cont_line = False

   while gotOK < 50:
       reply = reader.stdout.readline()
       # print "reply: %s" % reply
       if re.match("^>.*$", reply):
           process_line(line)
           line = reply.rstrip()
           cont_line = True
           # print 'start line: ' + line
           gotOK += 1
       elif re.match("^\s\s\w.*$", reply):
           line = line + reply.rstrip()
           # print 'line: ' + line




if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print '\nInterrupt caught'

    finally:
        # Close opend file
        # fo.close()
        pass
