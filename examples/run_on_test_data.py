"""
Example of how to read and process previously captured data.
This is useful for doing testing without having beacons available.
"""
from scanner import protocols
from scanner.company_id import lookup
from scanner.service_class_uuids import lookup_16bit
from tests.data.pkt_capture import more_beacons as data


def build_by_report_type():
    """Group test data by type of HCI advertising report"""
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
    return adv_zero, adv_one, adv_two, adv_three, adv_four


def print_by_report_type(reports):
    """Print key information from the different advertisement reports"""
    for i, style in enumerate(reports):
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

            payload = protocols.AdvertData(list(entry.values())[0])
            if payload.adv_flags:
                print(f'\t\tFlags - {payload.adv_flags}')
            if payload.manufacturer_data:
                print(f'\t\t\t{lookup(payload.mfg_id)}({payload.mfg_id:#06x}):'
                      f' {payload.manufacturer_data}')
            elif payload.service_data:
                print(
                    f'\t\t\t{lookup_16bit(payload.service_id)}'
                    f'({payload.service_id:#06x}): {payload.service_data}')


if __name__ == '__main__':
    rpts = build_by_report_type()
    print_by_report_type(rpts)
