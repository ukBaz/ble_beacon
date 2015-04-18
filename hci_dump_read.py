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

        
def mac_address(bytes):
    # bytes[13] ":" bytes[12] ":" bytes[11] ":" bytes[10] ":" bytes[9] ":" bytes[8]
    address = '{0}:{1}:{2}:{3}:{4}:{5}'.format(bytes[12], bytes[11],
                            bytes[10], bytes[9], bytes[8], bytes[7])
    return address

def service(data):
    # Complete List of 16-Dit Service
    pass

def service_id(data):
    # Assigned Uri Service UUID
    # 0xFED8
    pass

def ad_length(data):
    # Between 5 - 23
    return int(data[21], 16)

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

def tx_power(data):
    # Reference power from beacon broadcast
    tx_power = int(data[26], 16)
    if tx_power & 0x80: # MSB set -> neg.
        return -((~tx_power & 0xff) + 1)
    else:
        return tx_power

def uri_scheme(data):
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
    return encode_scheme[int(data[27])]

def encoded_uri(data, length):
    # Uri content
    val = ''
    for i in data[28:(22 + length)]:
        # print 'Encode: {0} - {1}'.format(i, chr(int(i, 16)))
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
    return (data[17] == '03' and
            data[18] == '03' and
            data[19] == 'D8' and
            data[20] == 'FE')

gotOK = False
cmd = './hcidump.sh'
print cmd
reader = subprocess.Popen(cmd, 
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )

line = '' 
cont_line = False
while not gotOK:
    reply = reader.stdout.readline()
    # print "reply: %s" % reply
    if re.match(".*>.*", reply):
        line = reply.rstrip()
        cont_line = True
    elif cont_line :
        line = line +  reply.rstrip()
        print 'line: ' + line
        mydata = line.split()
        if mydata[0] == '>':
            del mydata[0]
        if has_uribeacon_service(mydata):
            print mydata[-1]
            print 'TX power: {}'.format(tx_power(mydata))
            print 'RSSI: {}'.format(rssi_value(mydata))
            print 'Address: {}'.format(mac_address(mydata))
            print 'Length: {}'.format(ad_length(mydata))
            print 'uri: {}{}'.format(uri_scheme(mydata), encoded_uri(mydata, ad_length(mydata)))
