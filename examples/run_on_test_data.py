from scanner import protocols
from scanner.company_id import lookup
from scanner.service_class_UUIDs import lookup_16bit
from tests.data.pkt_capture import more_beacons as data


def process_ad_payload(data):
    payload_length = data[0]
    pointer = 1
    ad_type = None
    ad_data = None
    while pointer < payload_length:
        data_len = data[pointer]
        next_pointer = pointer + data[pointer] + 1
        ad_type = data[pointer + 1]
        ad_data = data[pointer + 2: next_pointer]
        print(f'\t\tType: {ad_type} - {protocols.DATA_TYPE[ad_type]}')
        if ad_type == 0xff:
            mfg_id = int.from_bytes(ad_data[0:2], byteorder='little')
            print(f'\t\t\t{lookup(mfg_id)}({mfg_id:#06x}): {ad_data[2:]}')
        elif ad_type == 0x03 or ad_type == 0x16:
            service_id = int.from_bytes(ad_data[0:2], byteorder='little')
            print(f'\t\t\t{lookup_16bit(service_id)}({service_id:#06x}): {ad_data[2:]}')
        else:
            print(f'\t\t\tData: {ad_data}')
        pointer = next_pointer


adv_zero = []
adv_one = []
adv_two = []
adv_three = []
adv_four = []
for pkt in data:
    if pkt[0] == 0x04 and pkt[1] == 0x3e and pkt[3] == 0x02:
        mac_addr = str(protocols.MacAddress(pkt[7:13]))
        if pkt[5] == 0x00:
            adv_zero.append({mac_addr: pkt[13:-1]})
        elif pkt[5] == 0x01:
            adv_one.append({mac_addr: pkt[13:-1]})
        elif pkt[5] == 0x02:
            adv_two.append({mac_addr: pkt[13:-1]})
        elif pkt[5] == 0x03:
            adv_three.append({mac_addr: pkt[13:-1]})
        elif pkt[5] == 0x04:
            adv_four.append({mac_addr: pkt[13:-1]})

    # assert x[byte] == 0x3e

for i, style in enumerate([adv_zero, adv_one, adv_two, adv_three, adv_four]):
    print(f'\nEvent type {i}: {protocols.ADV_RPT_TYPE_LOOKUP[i]}')
    for entry in style:
        beacon = 'Unknown Beacon'
        if b'\xff\x33\x01' in list(entry.values())[0]:
            beacon = 'Blue Maestro'
        elif b'\xff\xff\xff\xbe\xac' in list(entry.values())[0]:
            beacon = 'Alt Beacon'
        elif b'\xaa\xfe\x10' in list(entry.values())[0]:
            beacon = 'Eddystone - URL'
        elif b'\xaa\xfe\x00' in list(entry.values())[0]:
            beacon = 'Eddystone - UID'
        elif b'\xff\x4c\x00\x02' in list(entry.values())[0]:
            beacon = 'iBeacon'
        print(f'\t{list(entry.keys())[0]} - {beacon}')
        process_ad_payload(list(entry.values())[0])
