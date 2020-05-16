import struct
import uuid
from scanner.company_id import company_name
EVT_LE_META_EVENT = 0x3E


class AdvertEventHandler:

    def __init__(self, pkt):
        self.pkt = pkt
        self.adv_data = None
        self.manf_data = None
        self.serv_data = None
        self.eddystone_url = None
        self.eddystone_uid = None
        self.ibeacon = None
        self.alt_beacon = None

        self.evt = AdvertEvent(pkt)
        if self.evt.is_le_meta_event and self.evt.payload:
            self.adv_payload = AdvertPayload(self.evt.payload)
            self.rssi = self.evt.rssi
        else:
            return
        if self.adv_payload.adv_data is not None:
            self.adv_data = AdvertData(self.adv_payload.adv_data)
        if self.adv_data and self.adv_data.manufacturer_data:
            self.manf_data = ManufacturerData(self.adv_data.manufacturer_data)
            if self.manf_data.is_ibeacon:
                self.ibeacon = iBeacon(self.manf_data.data)
            elif self.manf_data.is_alt_beacon:
                self.alt_beacon = AltBeacon(self.manf_data.data)
        elif self.adv_data and self.adv_data.service_data:
            self.serv_data = ServiceData(self.adv_data.service_data)
            self.eddystone_beacon = Eddystone(self.serv_data.service_data)
            if self.eddystone_beacon.is_eddystone_url:
                self.eddystone_url = EddystoneUrl(self.eddystone_beacon.data)
            elif self.eddystone_beacon.is_eddystone_uid:
                self.eddystone_uid = EddystoneUid(self.eddystone_beacon.data)

    @property
    def address(self):
        return self.adv_payload.mac_addr.__str__()

    @property
    def advert_flags(self):
        return self.adv_payload.adv_flags

    def __repr__(self):
        data = '[{}]'.format(', '.join(hex(x) for x in self.pkt))
        return f'<AdvertEventHandler(bytearray({data}))>'


class AdvertEvent:

    def __init__(self, pkt=None):
        self.data_in = pkt
        self.payload = None
        self.pkt_len = None
        self.pkt_type = None
        self.event = None
        self.rssi = None
        if pkt is not None:
            self.pkt_type, self.event, self.pkt_len = struct.unpack(
                'BBB', pkt[:3])
            self.rssi = int.from_bytes([pkt[-1]], 'big', signed=True)
            if self.event == EVT_LE_META_EVENT and self.pkt_len > 12:
                self.payload = pkt[3:-1]

    @property
    def is_le_meta_event(self):
        return self.event == EVT_LE_META_EVENT

    def __repr__(self):
        return f'<AdvertEvent({self.data_in})>'


class AdvertPayload:
    def __init__(self, data):
        self.data_in = data
        le_ad_rpt_length = data[0]
        rpt_count = data[1]
        ad_evt_type = data[2]
        addr_type = data[3]
        self.mac_addr = MacAddress(data[4:11])
        if ad_evt_type == 0x03:
            self.adv_flags = AdvertFlags(data[11:14])
            self.adv_data = data[14:]
        else:
            self.adv_flags = None
            self.adv_data = data[11:]

    def __str__(self):
        return f'<AdvertPayload {self.mac_addr} {self.adv_flags} {self.adv_data}'

    def __repr__(self):
        return f'<AdvertPayload({self.data_in})>'


class MacAddress:
    def __init__(self, data):
        self._mac_address = reversed(data)

    def __str__(self):
        return ':'.join([f'{q:02x}' for q in self._mac_address])

    def __repr__(self):
        return f'<MacAddress({bytearray(reversed(self._mac_address))}>'


class AdvertFlags:
    def __init__(self, data):
        self.length, self.type, self.data = data

    def __repr__(self):
        return f'<AdvertFlags {self.length}, {self.type}, {self.data}>'


class AdvertData:
    def __init__(self, data):
        self.manufacturer_data = None
        self.service_data = None
        self.length = data[0]
        self.type = data[1]
        # 0xff is Manufacturer data. 0x03 is service data
        if self.type == 0xff:
            self.manufacturer_data = data[2:]
        elif self.type == 0x03:
            self.service_data = data[2:]

    def __str__(self):
        return f'<AdvertData {self.type} >'

    def __repr__(self):
        return f'<AdvertData {self.type} >'


class ManufacturerData:
    def __init__(self, data):
        self.is_ibeacon = False
        self.is_alt_beacon = False
        self.mfg_id = int.from_bytes(data[0:2], byteorder='little')
        self.manufacturer = lookup_company_name(self.mfg_id)
        self.type = data[2]
        self.beacon_code = int.from_bytes(data[2:4], byteorder='little')
        self.is_ibeacon = all((self.mfg_id == 0x004c, self.type == 0x02))
        self.is_alt_beacon = self.beacon_code == 0xacbe
        self.data = data

    def __repr__(self):
        return f'<Manufacturer {self.manufacturer} >'


class ServiceData:
    def __init__(self, data):
        self.beacon = None
        self.service_uuid = int.from_bytes(data[0:2], byteorder='little')
        self.length = data[2]
        self.type = data[3]
        self.service_data = data[4:]

    def __repr__(self):
        return self.beacon.__repr__()


class iBeacon:
    def __init__(self, data):
        self.mfg_id = int.from_bytes(data[0:2], byteorder='little')
        self.manufacturer = lookup_company_name(self.mfg_id)
        self.type = data[2]
        self.length = data[3]
        self._beacon_uuid = uuid.UUID(bytes=data[4:20])
        self.major = int.from_bytes(data[20:22], 'big', signed=False)
        self.minor = int.from_bytes(data[22:24], 'big', signed=False)
        self.tx_pwr = int.from_bytes([data[24]], 'big', signed=True)

    @property
    def beacon_uuid(self):
        return str(self._beacon_uuid)

    def __repr__(self):
        return f'<iBeacon {self.beacon_uuid}, {self.major}, ' \
               f'{self.minor}, {self.tx_pwr}'


class AltBeacon:
    def __init__(self, data):
        self.mfg_id = int.from_bytes(data[0:2], byteorder='little')
        self.manufacturer = lookup_company_name(self.mfg_id)
        self._beacon_uuid = uuid.UUID(bytes=data[4:20])
        self.tx_pwr = int.from_bytes([data[-2]], 'big', signed=True)
        self.mfg_reserved = data[-1]

    @property
    def beacon_uuid(self):
        return str(self._beacon_uuid)


class Eddystone:
    def __init__(self, data):
        self.is_eddystone_beacon = False
        self.is_eddystone_url = False
        self.eddystone_uuid = int.from_bytes(data[0:2], byteorder='little')
        self.frame_type = data[2]
        self.is_eddystone_beacon = self.eddystone_uuid == 0xFEAA
        self.is_eddystone_url = self.frame_type == 0x10
        self.is_eddystone_uid = self.frame_type == 0x00

        self.data = data[3:]

    def __repr__(self):
        return f'<Eddystone {self.eddystone_uuid:#02x}, ' \
               f'{self.frame_type:#02x}, ' \
               f'{self.beacon.url}>'


class EddystoneUrl:

    def __init__(self, data):
        self._url_prefix_scheme = ['http://www.', 'https://www.', 
                                  'http://', 'https://', ]
        self._url_encoding = ['.com/', '.org/', '.edu/', '.net/', '.info/',
                              '.biz/', '.gov/', '.com', '.org', '.edu',
                              '.net', '.info', '.biz', '.gov']
        self.tx_pwr, self.prefix = struct.unpack('bB', data[0:2])
        self.encoded_url = data[2:]

    @property
    def url(self):
        full_url = self._url_prefix_scheme[self.prefix]
        for letter in self.encoded_url:
            if letter < len(self._url_encoding):
                full_url += self._url_encoding[letter]
            else:
                full_url += chr(letter)
        return full_url
        
    def __repr__(self):
        return f'<EddystoneUrl {self.tx_pwr} {self.prefix} {str(self.encoded_url)}>'


class EddystoneUid:

    def __init__(self, data):
        self.tx_pwr = int.from_bytes([data[0]], 'big', signed=True)
        self.namespace_id = int.from_bytes(data[1:11], 'big')
        self.instance_id = int.from_bytes(data[11:17], 'big')


def lookup_company_name(company_id):
        try:
            manufacturer = company_name[company_id]
        except IndexError:
            manufacturer = 'No name available'
        return manufacturer
