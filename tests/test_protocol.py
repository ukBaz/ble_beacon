import pytest
from tests.data import pkt_capture
from scanner import protocols


def idfn(val):
    return sum(val)


@pytest.mark.parametrize('packet', pkt_capture.data, ids=idfn)
def test_all_pkts(packet):
    print(f'\n{packet}')
    try:
        advert = protocols.AdvertEventHandler(packet)
    except Exception:
        pytest.fail('Unexpected exception')


@pytest.mark.parametrize('packet', pkt_capture.bytes_only, ids=idfn)
def test_get_mac_address(packet):
    print(f'\n{packet}')
    advert = protocols.AdvertEventHandler(packet)
    assert advert.address == ':'.join([f'{q:02x}'
                                      for q in reversed(packet[7:14])])


@pytest.mark.parametrize('packet', pkt_capture.bytes_only, ids=idfn)
def test_get_adv_flags(packet):
    print(f'\n{packet}')
    advert = protocols.AdvertEventHandler(packet)
    if packet[14] == 0x02:
        assert advert.adv_payload.adv_flags.length == packet[14]
    else:
        assert advert.adv_payload.adv_flags is None


@pytest.mark.parametrize('packet', pkt_capture.bytes_only, ids=idfn)
def test_serv_data(packet):
    print(f'\n{packet}')
    advert = protocols.AdvertEventHandler(packet)
    if b'\x03\x03' in packet:
        assert advert.serv_data is not None
    else:
        assert advert.serv_data is None


@pytest.mark.parametrize('packet', pkt_capture.bytes_only, ids=idfn)
def test_manf_data(packet):
    print(f'\n{packet}')
    advert = protocols.AdvertEventHandler(packet)
    if b'\xff\x4c\x00\x02' in packet or b'\xff\xff\xff\xbe\xac' in packet:
        assert advert.manf_data is not None
    else:
        assert advert.manf_data is None


@pytest.mark.parametrize('packet', pkt_capture.bytes_only, ids=idfn)
def test_eddy_url_url(packet):
    expected_urls = ['https://www.firstuk.org/', 'https://ukbaz.github.io']
    print(f'\n\n\t{packet}, {expected_urls}')
    advert = protocols.AdvertEventHandler(packet)
    if b'\xaa\xfe\x10' in packet:
        print(f'\n\n\teddystone url: {advert.eddystone_url.url}')
        assert advert.eddystone_url.url in expected_urls
    else:
        assert advert.eddystone_url is None


@pytest.mark.parametrize('packet', pkt_capture.bytes_only, ids=idfn)
def test_eddy_tx_pwr(packet):
    expected_urls = ['https://www.firstuk.org/', 'https://ukbaz.github.io']
    print(packet)
    advert = protocols.AdvertEventHandler(packet)
    if b'\xaa\xfe\x10' in packet:
        print(f'tx pwr = {advert.eddystone_url.tx_pwr}')
        assert type(advert.eddystone_url.tx_pwr) is int
    else:
        assert advert.eddystone_url is None


@pytest.mark.parametrize('packet', pkt_capture.bytes_only, ids=idfn)
def test_ibeacon(packet):
    expected_tx_pwr = [-65]
    expected_majors = [278]
    expected_minors = [872]
    expected_uuids = ['6ab17c17-f47b-4d41-8036-526aeed22f73']
    print(packet)
    advert = protocols.AdvertEventHandler(packet)
    if b'\xff\x4c\x00\x02' in packet:
        print(f'tx pwr = {advert.ibeacon.tx_pwr}')
        assert advert.ibeacon.tx_pwr in expected_tx_pwr
        assert advert.ibeacon.major in expected_majors
        assert advert.ibeacon.minor in expected_minors
        assert advert.ibeacon.beacon_uuid in expected_uuids
    else:
        assert advert.ibeacon is None


@pytest.mark.parametrize('packet', pkt_capture.bytes_only, ids=idfn)
def test_alt_beacon(packet):
    expected_tx_pwr = [-68]
    expected_uuids = ['48253e59-7224-4463-b9b8-033ffab58104']
    print(packet)
    advert = protocols.AdvertEventHandler(packet)
    if b'\xff\xff\xff\xbe\xac' in packet:
        print(f'tx pwr = {advert.alt_beacon.tx_pwr}')
        assert advert.alt_beacon.tx_pwr in expected_tx_pwr
        assert advert.alt_beacon.beacon_uuid in expected_uuids
        assert advert.alt_beacon.manufacturer == 'No name available'
    else:
        assert advert.alt_beacon is None


def test_not_le_meta_evt():
    ad = protocols.AdvertEventHandler(b'\x04\x0f\x04\x00\x01\x01\x04')
    assert not ad.evt.is_le_meta_event


def test_evt_hndlr_repr():
    ad = protocols.AdvertEventHandler(
        b'\x04\x3e\x26\x02\x01\x02\x01\xf9u\xa8r\x14r\x1a\x03\x03\xaa\xfe\x15'
        b'\x16\xaa\xfe\x00\xbf\xfb\x35\xfd\r\x17\x69\x1d\x64\xaa\x90\xab\xcd'
        b'\xef\t\x87\x65\xc0')
    assert repr(ad).startswith('<AdvertEventHandler(bytearray([0x04, 0x3e, 0x')


def test_evt_hndlr_flags():
    ad = protocols.AdvertEventHandler(
        b'\x04\x3e\x29\x02\x01\x03\x01\xbe\x43\xe7\x35\x82\xde\x1d\x02\x01\x06'
        b'\x03\x03\xaa\xfe\x15\x16\xaa\xfe\x10\xf6\x03\x75\x6b\x62\x61\x7a\x2e'
        b'\x67\x69\x74\x68\x75\x62\x2e\x69\x6f\xbd')
    assert repr(ad.advert_flags) == ('<AdvertFlags(bytearray('
                                     '[0x02, 0x01, 0x06])>')


def test_ad_evt_repr():
    evt = protocols.AdvertEvent(b'\x04>\x0c\x02\x01\x04\x01\n\t9\x1b'
                                b'\xf6y\x00\xb5')
    assert repr(evt).startswith('<AdvertEvent(bytearray([0x04, 0x3e,')


def test_ad_payload_repr():
    payload = protocols.AdvertPayload(b'\x02\x01\x03\x01\xbeC\xe75\x82\xde\x1d'
                                      b'\x02\x01\x06\x03\x03\xaa\xfe\x15\x16'
                                      b'\xaa\xfe\x10\xf6\x03ukbaz.github.io')
    assert repr(payload).startswith('<AdvertPayload(bytearray([0x02, 0x01, 0x')
    assert str(payload).startswith('<AdvertPayload 1d:de:82:35:e7:43:be')


def test_ad_data_repr():
    adv_data = protocols.AdvertData(b'\x03\x03\xaa\xfe\x15\x16\xaa\xfe\x10'
                                    b'\xf6\x03ukbaz.github.io')
    assert repr(adv_data).startswith('<AdvertData(bytearray([0x03, 0x03, 0xaa,')
    assert str(adv_data).startswith('<AdvertData 0x3 0x3 >')


def test_manuf_data_alt():
    md = protocols.ManufacturerData(b'\xff\xff\xbe\xacH%>Yr$Dc\xb9\xb8\x03?'
                                    b'\xfa\xb5\x81\x04\x00{\x01A\xbc\x00')
    assert repr(md).startswith('<ManufacturerData(bytearray([0xff, 0xff, 0xbe')
    assert str(md).startswith('<Manufacturer No name available >')


def test_manuf_data_ibeacon():
    md = protocols.ManufacturerData(b'L\x00\x02\x15j\xb1|\x17\xf4{MA\x806Rj'
                                    b'\xee\xd2/s\x01\x16\x03h\xbf')
    assert repr(md).startswith('<ManufacturerData(bytearray([0x4c, 0x00, 0x02')
    assert str(md).startswith('<Manufacturer Apple, Inc. >')


def test_srv_data():
    md = protocols.ServiceData(b'\xaa\xfe\x15\x16\xaa\xfe\x10\xf6'
                               b'\x03ukbaz.github.io')
    assert repr(md).startswith('<ServiceData(bytearray([0xaa, 0xfe, 0x15, 0x')
    assert str(md).startswith('<ServiceData(bytearray([0xaa, 0xfe, 0x15, 0x16')


def test_ibeacon_repr():
    ib = protocols.iBeacon(b'L\x00\x02\x15j\xb1|\x17\xf4{MA\x806Rj\xee\xd2/s'
                           b'\x01\x16\x03h\xbf')
    assert repr(ib).startswith('<iBeacon(bytearray([0x4c, 0x00, 0x02,')
    assert str(ib).startswith('<iBeacon 6ab17c17-f47b-4d41-8036-526aeed22f73,')


def test_alt_beacon_repr():
    md = protocols.AltBeacon(b'\xff\xff\xbe\xacH%>Yr$Dc\xb9\xb8\x03?'
                             b'\xfa\xb5\x81\x04\x00{\x01A\xbc\x00')
    assert repr(md).startswith('<AltBeacon(bytearray([0xff, 0xff, 0xbe, 0xac')
    assert str(md).startswith('<AltBeacon No name available 48253e59-7224-')


def test_eddystone():
    eddy = protocols.Eddystone(b'\xaa\xfe\x10\xf6\x03ukbaz.github.io')
    assert repr(eddy).startswith('<Eddystone(bytearray([0xaa, 0xfe, 0x10, 0x')
    assert str(eddy).startswith("<Eddystone 0xfeaa, 0x10, b'\\xf6"
                                "\\x03ukbaz.github.io'>")


def test_eddy_url():
    eddy = protocols.EddystoneUrl(b'\xaa\xfe\x10\xf6\x03ukbaz.github.io')
    assert repr(eddy).startswith('<EddystoneUrl(bytearray([0xaa, 0xfe, 0x10, 0x')
    assert str(eddy).startswith("<EddystoneUrl -86 254 b'\\x10\\xf6"
                                "\\x03ukbaz.github.io'>")


def test_eddy_uid():
    eddy = protocols.EddystoneUid(b'\xaa\xfe\x00\xbf\xfb\x35\xfd\r\x17\x69'
                                  b'\x1d\x64\xaa\x90\xab\xcd\xef\t\x87\x65')
    assert repr(eddy).startswith('<EddystoneUid(bytearray([0xaa, 0xfe, 0x00')
    assert str(eddy).startswith('<EddystoneUid -86 1199494920358931245525277 '
                                '110683734396399>')



def test_mac_addr():
    # mac = protocols.MacAddress(b'\xe4\xa4\x71\x63\xe1\x69')
    mac = protocols.MacAddress(b'\xbe\x43\xe7\x35\x82\xde')
    assert str(mac) == 'de:82:35:e7:43:be'


def test_mac_addr_repr():
    # mac = protocols.MacAddress(b'\xe4\xa4\x71\x63\xe1\x69')
    mac = protocols.MacAddress(b'\xbe\x43\xe7\x35\x82\xde')
    assert repr(mac) == ('<MacAddress(bytearray([0xbe, 0x43, 0xe7,' 
                         ' 0x35, 0x82, 0xde])>')


def test_advert_flags():
    flags = protocols.AdvertFlags(b'\x02\x01\x06')
    assert flags.length == 2
    assert flags.type == 1
    assert flags.data == 6


def test_eddystone_url():
    eddy_url = protocols.EddystoneUrl(b'\xbd\x03ukbaz.github.io')
    assert eddy_url.url == "https://ukbaz.github.io"


def test_eddystone_tx_pwr():
    eddy_url = protocols.EddystoneUrl(b'\xbd\x03ukbaz.github.io')
    assert eddy_url.tx_pwr == -67
