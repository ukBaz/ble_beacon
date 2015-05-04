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
import numpy as np

        
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
    return int(data[18], 16)

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
    tx_power = int(data[23], 16)
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
    return encode_scheme[int(data[24])]

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

def encoded_uri(data, length):
    # Uri content
    val = ''
    for i in data[25:(25 + length - 6)]:
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

 
def holt_winters_second_order_ewma( x, span, beta ):
    """
    http://connor-johnson.com/2014/02/01/smoothing-with-exponentially-weighted-moving-averages/
    """
    N = x.size
    alpha = 2.0 / ( 1 + span )
    s = np.zeros(( N, ))
    b = np.zeros(( N, ))
    s[0] = x[0]
    for i in range( 1, N ):
        s[i] = alpha * x[i] + ( 1 - alpha )*( s[i-1] + b[i-1] )
        b[i] = beta * ( s[i] - s[i-1] ) + ( 1 - beta ) * b[i-1]
    return s
 
def calc_distance(rssi, tx_value):
    # Power value. Usually ranges between -59 to -65
    # tx_value = -69
    if rssi == 0:
        return -1.0
    
    ratio = rssi*1.0/tx_value
    if ratio < 1.0:
        return round(math.pow(ratio,10), 2)
    else:
        distance =  (0.89976)*math.pow(ratio,7.7095) + 0.111
        return round(distance, 2)


if __name__ == '__main__':
   gotOK = True
   # Open a file
   # fo = open("logging.txt", "wb")
   cmd = './hcidump.sh'
   print cmd
   reader = subprocess.Popen(cmd, 
                           shell=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           )

   line = '' 
   cont_line = False
   try:
      while gotOK < 50:
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
              # print mydata[14]
              if has_uribeacon_service(mydata):
                  print mydata[-1]
                  print 'Address: {}'.format(mac_address(mydata))
                  print 'uri: {}{}'.format(uri_scheme(mydata),
                                           encoded_uri(mydata, ad_length(mydata)))
                  print 'TX power: {}'.format(tx_power(mydata))
                  print 'RSSI: {}'.format(rssi_value(mydata))
                  print 'distance: {}'.format(calc_distance(rssi_value(mydata),
                                                            tx_power(mydata)))
                  print 'Length: {}'.format(ad_length(mydata))
                  # fo.write( '{0},'.format(rssi_value(mydata)))
                  gotOK += 1
          

   except KeyboardInterrupt:
      print '\nInterrupt caught'

   finally:
      # Close opend file
      # fo.close()
        pass
