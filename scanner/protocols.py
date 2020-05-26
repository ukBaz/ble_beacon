"""
Unpack beacon advertising packets

pkt[0] = Packet Type (Filter ensures we only get 0x04) Is packet type?
pkt[1] = HCI event type (We only interested in 0x3e?) LE Meta Event
pkt[2] = Length of packet
pkt[3] = LE Meta Event sub event (see LE_META_EVENT_LOOKUP)
pkt[4] = Number of reports in packet
pkt[5] = Advertisement Report Event Type (see ADV_RPT_TYPE_LOOKUP)
pkt[6] = Address Type (see ADDRESS_TYPE_LOOKUP)
pkt[7:13] = Mac address
pkt[13:] = Advert packet information
"""
import struct
import uuid
from scanner.company_id import lookup
from scanner.service_class_UUIDs import lookup_16bit

EVT_LE_META_EVENT = 0x3E
LE_META_EVENT_LOOKUP = {
    0x01: "LE Connection Complete",
    0x02: "LE Advertising Report",
    0x03: "LE Connection Update Complete",
    0x04: "LE Read Remote Used Features",
    0x05: "LE Long Term Key Request",
    0x06: "LE Remote Connection Parameter Request",
    0x07: "LE Data Length Change",
    0x08: "LE Read Local P-256 Public Key Complete",
    0x09: "LE Generate DHKey Complete",
    0x0a: "LE Enhanced Connection Complete",
    0x0b: "LE Direct Advertising Report",
    0x0c: "LE PHY Update Complete",
    0x0d: "LE Extended Advertising Report",
    0x0e: "LE Periodic Advertising Sync Established",
    0x0f: "LE Periodic Advertising Report",
    0x10: "LE Periodic Advertising Sync Lost",
    0x11: "LE Scan Timeout",
    0x12: "LE Advertising Set Terminated",
    0x13: "LE Scan Request Received",
    0x14: "LE Channel Selection Algorithm"}
ADV_RPT_TYPE_LOOKUP = {
    0x00: "Connectable undirected - ADV_IND",
    0x01: "Connectable directed - ADV_DIRECT_IND",
    0x02: "Scannable undirected - ADV_SCAN_IND",
    0x03: "Non connectable undirected - ADV_NONCONN_IND",
    0x04: "Scan response - SCAN_RSP"}
ADDRESS_TYPE_LOOKUP = {
    0x00: 'Public',
    0x01: 'Random',
    0x02: 'Resolved Public',
    0x03: 'Resolved Random'}
DATA_TYPE = {
    0x01: "Flags",
    0x02: "Incomplete List of 16-bit Service Class UUIDs",
    0x03: "Complete List of 16-bit Service Class UUIDs",
    0x04: "Incomplete List of 32-bit Service Class UUIDs",
    0x05: "Complete List of 32-bit Service Class UUIDs",
    0x06: "Incomplete List of 128-bit Service Class UUIDs",
    0x07: "Complete List of 128-bit Service Class UUIDs",
    0x08: "Shortened Local Name",
    0x09: "Complete Local Name",
    0x0A: "Tx Power Level",
    0x0D: "Class of Device",
    0x0E: "Simple Pairing Hash C",
    0x0F: "Simple Pairing Randomizer R",
    0x10: "Device ID",
    0x11: "Security Manager Out of Band Flags",
    0x12: "Slave Connection Interval Range",
    0x14: "List of 16-bit Service Solicitation UUIDs",
    0x15: "List of 128-bit Service Solicitation UUIDs",
    0x16: "Service Data - 16-bit UUID",
    0x17: "Public Target Address",
    0x18: "Random Target Address",
    0x19: "Appearance",
    0x1A: "Advertising Interval",
    0x1B: "LE Bluetooth Device Address",
    0x1C: "LE Role",
    0x1D: "Simple Pairing Hash C-256",
    0x1E: "Simple Pairing Randomizer R-256",
    0x1F: "List of 32-bit Service Solicitation UUIDs",
    0x20: "Service Data - 32-bit UUID",
    0x21: "Service Data - 128-bit UUID",
    0x22: "LE Secure Connections Confirmation Value",
    0x23: "LE Secure Connections Random Value",
    0x24: "URI",
    0x25: "Indoor Positioning",
    0x26: "Transport Discovery Data",
    0x27: "LE Supported Features",
    0x28: "Channel Map Update Indication",
    0x29: "PB-ADV",
    0x2A: "Mesh Message",
    0x2B: "Mesh Beacon",
    0x2C: "BIGInfo",
    0x2D: "Broadcast_Code",
    0x3D: "3D Information Data",
    0xFF: "Manufacturer Specific Data"
}


class AdvertEventHandler:
    """Class to unpack BLE advert event"""
    def __init__(self, pkt):
        self.pkt = pkt
        self.adv_data = None
        self.mac_address = None
        self.rssi = None
        self.manf_data = None
        self.serv_data = None
        self.eddystone_url = None
        self.eddystone_uid = None
        self.ibeacon = None
        self.alt_beacon = None

        self.evt = AdvertEvent(pkt)
        if not self.evt.payload:
            return
        self.rssi = self.evt.rssi
        self.adv_payload = self.evt.payload
        self.adv_data = AdvertData(self.adv_payload)
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
        return self.evt.mac_addr.__str__()

    @property
    def advert_flags(self):
        """Get advertisement flags from packet"""
        return self.adv_data.adv_flags

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
        self.pkt_type = pkt[0]
        self.event = pkt[1]
        self.pkt_len = pkt[2]
        self.sub_evt = pkt[3]
        self.rpt_count = pkt[4]
        if (
                self.pkt_type == 0x04 and
                self.event == 0x3e and
                self.sub_evt == 0x02
        ):
            # sub_evt 0x02 = LE Advertising Report
            self.rssi = int.from_bytes([pkt[-1]], 'big', signed=True)
            self.adv_rpt_type = pkt[5]
            self.address_type = pkt[6]
            self.mac_addr = MacAddress(pkt[7:13])
            self.payload = pkt[13:-1]

    @property
    def is_le_meta_event(self):
        """method to see if BLE advertising event"""
        return self.event == EVT_LE_META_EVENT

    def __repr__(self):
        return f'<AdvertEvent({_format_bytearray(self.data_in)})>'


# class AdvertPayload:
#     """Class to unpack Bluetooth advertising payload"""
#     def __init__(self, data):
#         self.data_in = data
#         # LE Advertising Report = 0x02
#         sub_event = data[0]
#         rpt_count = data[1]
#         ad_evt_type = data[2]
#         addr_type = data[3]
#         self.mac_addr = MacAddress(data[4:11])
#         if ad_evt_type == 0x03:
#             self.adv_flags = AdvertFlags(data[11:14])
#             self.adv_data = data[14:]
#         else:
#             self.adv_flags = None
#             self.adv_data = data[11:]
#
#     def __str__(self):
#         return (f'<AdvertPayload {self.mac_addr}, {self.adv_flags}, '
#                 f'{self.adv_data}>')
#
#     def __repr__(self):
#         return f'<AdvertPayload({_format_bytearray(self.data_in)})>'


class MacAddress:
    """Class to unpack Bluetooth mac address for beacon device"""
    def __init__(self, data):
        self.data_in = data
        self._mac_address = reversed(data)

    def __str__(self):
        return ':'.join([f'{q:02x}' for q in self._mac_address])

    def __repr__(self):
        return f'<MacAddress({_format_bytearray(self.data_in)}>'


class AdvertData:
    """
    Class to unpack Bluetooth Service Data
    https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile/
    """
    def __init__(self, data):
        self.data_in = data
        self.adv_flags = None
        self.manufacturer_data = None
        self.service_data = None
        payload_length = data[0]
        pointer = 1
        ad_type = None
        ad_data = None
        while pointer < payload_length:
            data_len = data[pointer]
            next_pointer = pointer + data[pointer] + 1
            ad_type = data[pointer + 1]
            ad_data = data[pointer + 2: next_pointer]
            if ad_type == 0xff:
                mfg_id = int.from_bytes(ad_data[0:2], byteorder='little')
                self.manufacturer_data = ad_data
            elif ad_type == 0x16:
                service_id = int.from_bytes(ad_data[0:2], byteorder='little')
                self.service_data = ad_data
            elif ad_type == 0x01:
                self.adv_flags = ad_data
            pointer = next_pointer

    # def __str__(self):
    #     return f'<AdvertData {self.data_in[0]:#02x} {self.ad_type:#02x} >'

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
        self.service_data = data

    def __repr__(self):
        return f'<ServiceData({_format_bytearray(self.service_data)})>'


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
        self.is_eddystone_url = all([self.is_eddystone_beacon,
                                     self.frame_type == 0x10])
        self.is_eddystone_uid = all([self.is_eddystone_beacon,
                                     self.frame_type == 0x00])

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
    """Utility to present bytearray in a readable way"""
    # when printing bytearrays, some bytes are converted to characters.
    # Some people have found this confusing so printing them in such a way
    # that they will stay hex values.
    return 'bytearray([{}])'.format(', '.join(f'{data_byte:#04x}'
                                              for data_byte in data))
