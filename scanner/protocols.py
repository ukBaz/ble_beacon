"""
Unpack beacon advertising packets
"""
import struct
import uuid
from scanner.company_id import lookup

EVT_LE_META_EVENT = 0x3E


class AdvertEventHandler:
    """Class to unpack BLE advert event"""
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
        """get the mac address of the beacon"""
        return self.adv_payload.mac_addr.__str__()

    @property
    def advert_flags(self):
        """Get advertisement flags from packet"""
        return self.adv_payload.adv_flags

    def __repr__(self):
        return f'<AdvertEventHandler({_format_bytearray(self.pkt)})>'


class AdvertEvent:
    """Class to unpack BlueZ HCI Advert event"""
    def __init__(self, pkt=None):
        self.data_in = pkt
        self.payload = None
        self.pkt_len = None
        self.pkt_type = None
        self.event = None
        self.rssi = None
        self.pkt_type, self.event, self.pkt_len = struct.unpack('BBB', pkt[:3])
        self.rssi = int.from_bytes([pkt[-1]], 'big', signed=True)
        if self.event == EVT_LE_META_EVENT and self.pkt_len > 12:
            self.payload = pkt[3:-1]

    @property
    def is_le_meta_event(self):
        """method to see if BLE advertising event"""
        return self.event == EVT_LE_META_EVENT

    def __repr__(self):
        return f'<AdvertEvent({_format_bytearray(self.data_in)})>'


class AdvertPayload:
    """Class to unpack Bluetooth advertising payload"""
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
        return (f'<AdvertPayload {self.mac_addr}, {self.adv_flags}, '
                f'{self.adv_data}>')

    def __repr__(self):
        return f'<AdvertPayload({_format_bytearray(self.data_in)})>'


class MacAddress:
    """Class to unpack Bluetooth mac address for beacon device"""
    def __init__(self, data):
        self.data_in = data
        self._mac_address = reversed(data)

    def __str__(self):
        return ':'.join([f'{q:02x}' for q in self._mac_address])

    def __repr__(self):
        return f'<MacAddress({_format_bytearray(self.data_in)}>'


class AdvertFlags:
    """Class to unpack Bluetooth GAP advertising flags"""
    def __init__(self, data):
        self.data_in = data
        self.length, self.type, self.data = data

    def __str__(self):
        return f'<AdvertFlags {self.length}, {self.type}, {self.data}>'

    def __repr__(self):
        return f'<AdvertFlags({_format_bytearray(self.data_in)}>'


class AdvertData:
    """
    Class to unpack Bluetooth Service Data
    https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile/
    """
    def __init__(self, data):
        self.data_in = data
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
        return f'<AdvertData {self.length:#02x} {self.type:#02x} >'

    def __repr__(self):
        return f'<AdvertData({_format_bytearray(self.data_in)})>'


class ManufacturerData:
    """
    Class to unpack Bluetooth Manufacturer Specific Data
    https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile/
    """
    def __init__(self, data):
        self.is_ibeacon = False
        self.is_alt_beacon = False
        self.mfg_id = int.from_bytes(data[0:2], byteorder='little')
        self.manufacturer = lookup(self.mfg_id)
        self.type = data[2]
        self.beacon_code = int.from_bytes(data[2:4], byteorder='little')
        self.is_ibeacon = all((self.mfg_id == 0x004c, self.type == 0x02))
        self.is_alt_beacon = self.beacon_code == 0xacbe
        self.data = data

    def __str__(self):
        return f'<Manufacturer {self.manufacturer} >'

    def __repr__(self):
        return f'<ManufacturerData({_format_bytearray(self.data)})>'


class ServiceData:
    """
    Class to unpack Bluetooth Service Data
    https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile/
    """
    def __init__(self, data):
        self.data_in = data
        self.service_uuid = int.from_bytes(data[0:2], byteorder='little')
        self.length = data[2]
        self.type = data[3]
        self.service_data = data[4:]

    def __repr__(self):
        return f'<ServiceData({_format_bytearray(self.data_in)})>'


class iBeacon:
    """
    Class to unplack Apple's iBeacon format packets
    https://en.wikipedia.org/wiki/IBeacon#Packet_Structure_Byte_Map
    """
    def __init__(self, data):
        self.data_in = data
        self.mfg_id = int.from_bytes(data[0:2], byteorder='little')
        self.manufacturer = lookup(self.mfg_id)
        self.type = data[2]
        self.length = data[3]
        self._beacon_uuid = uuid.UUID(bytes=data[4:20])
        self.beacon_uuid = str(self._beacon_uuid)
        self.major = int.from_bytes(data[20:22], 'big', signed=False)
        self.minor = int.from_bytes(data[22:24], 'big', signed=False)
        self.tx_pwr = int.from_bytes([data[24]], 'big', signed=True)

    def __str__(self):
        return f'<iBeacon {self.beacon_uuid}, {self.major}, ' \
               f'{self.minor}, {self.tx_pwr}>'

    def __repr__(self):
        return f'<iBeacon({_format_bytearray(self.data_in)})>'


class AltBeacon:
    """
    Class to unpack AltBeacon Packets
    https://github.com/AltBeacon/spec
    """
    def __init__(self, data):
        self.data_in = data
        self.mfg_id = int.from_bytes(data[0:2], byteorder='little')
        self.manufacturer = lookup(self.mfg_id)
        self._beacon_uuid = uuid.UUID(bytes=data[4:20])
        self.tx_pwr = int.from_bytes([data[-2]], 'big', signed=True)
        self.mfg_reserved = data[-1]

    @property
    def beacon_uuid(self):
        """method for displaying beacon uid as formatted string"""
        return str(self._beacon_uuid)

    def __str__(self):
        return (f'<AltBeacon {self.manufacturer} {self.beacon_uuid} '
                f'{self.tx_pwr}>')

    def __repr__(self):
        return f'<AltBeacon({_format_bytearray(self.data_in)})'


class Eddystone:
    """
    Class to unpack Eddystone frame header information
    https://github.com/google/eddystone/blob/master/protocol-specification.md
    """
    def __init__(self, data):
        self.data_in = data
        self.is_eddystone_beacon = False
        self.is_eddystone_url = False
        self.eddystone_uuid = int.from_bytes(data[0:2], byteorder='little')
        self.frame_type = data[2]
        self.is_eddystone_beacon = self.eddystone_uuid == 0xFEAA
        self.is_eddystone_url = self.frame_type == 0x10
        self.is_eddystone_uid = self.frame_type == 0x00

        self.data = data[3:]

    def __str__(self):
        return (f'<Eddystone {self.eddystone_uuid:#02x}, '
                f'{self.frame_type:#02x}, '
                f'{self.data}>')

    def __repr__(self):
        return f'<Eddystone({_format_bytearray(self.data_in)})>'


class EddystoneUrl:
    """
    Class to unpack Eddystone URL frames
    https://github.com/google/eddystone/tree/master/eddystone-url
    """
    def __init__(self, data):
        self.data_in = data
        self._url_prefix_scheme = ['http://www.', 'https://www.',
                                   'http://', 'https://', ]
        self._url_encoding = ['.com/', '.org/', '.edu/', '.net/', '.info/',
                              '.biz/', '.gov/', '.com', '.org', '.edu',
                              '.net', '.info', '.biz', '.gov']
        self.tx_pwr, self.prefix = struct.unpack('bB', data[0:2])
        self.encoded_url = data[2:]

    @property
    def url(self):
        """method to extract URL data from frame"""
        full_url = self._url_prefix_scheme[self.prefix]
        for letter in self.encoded_url:
            if letter < len(self._url_encoding):
                full_url += self._url_encoding[letter]
            else:
                full_url += chr(letter)
        return full_url

    def __str__(self):
        return (f'<EddystoneUrl {self.tx_pwr} {self.prefix} '
                f'{str(self.encoded_url)}>')

    def __repr__(self):
        return f'<EddystoneUrl({_format_bytearray(self.data_in)})>'


class EddystoneUid:
    """
    Class to unpack Eddystone UID frames
    https://github.com/google/eddystone/tree/master/eddystone-uid
    """
    def __init__(self, data):
        self.data_in = data
        self.tx_pwr = int.from_bytes([data[0]], 'big', signed=True)
        self.namespace_id = int.from_bytes(data[1:11], 'big')
        self.instance_id = int.from_bytes(data[11:17], 'big')

    def __str__(self):
        return (f'<EddystoneUid {self.tx_pwr} {self.namespace_id} '
                f'{self.instance_id}>')

    def __repr__(self):
        return f'<EddystoneUid({_format_bytearray(self.data_in)})>'


def _format_bytearray(data):
    """Utility to print bytearray in a readable way"""
    # when printing bytearrays, some bytes are converted to characters.
    # Some people have found this confusing so printing them in such a way
    # that they will stay hex values.
    return 'bytearray([{}])'.format(', '.join(f'{data_byte:#04x}'
                                              for data_byte in data))
