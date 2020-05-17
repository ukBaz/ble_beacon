import pytest
from tests.data import pkt_capture
from scanner import protocols


def idfn(val):
    return sum(val)


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
def test_eddy_url(packet):
    expected_urls = ['https://www.firstuk.org/', 'https://ukbaz.github.io']
    print(packet)
    advert = protocols.AdvertEventHandler(packet)
    if b'\xaa\xfe\x10' in packet:
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


@pytest.mark.parametrize('packet', pkt_capture.bytes_only, ids=idfn)
def test_repr(packet):
    expected_tx_pwr = [-68]
    expected_uuids = ['48253e59-7224-4463-b9b8-033ffab58104']
    print(f'\n{packet}')
    advert = protocols.AdvertEventHandler(packet)
    print(advert)
    print(advert.adv_data)
    print(advert.manf_data)
    print(advert.serv_data)
    print(advert.eddystone_url)
    print(advert.eddystone_uid)
    print(advert.ibeacon)
    print(advert.alt_beacon)
    print(advert.ibeacon.__repr__())


def test_mac_addr():
    # mac = protocols.MacAddress(b'\xe4\xa4\x71\x63\xe1\x69')
    mac = protocols.MacAddress(b'\xbe\x43\xe7\x35\x82\xde')
    assert str(mac) == 'de:82:35:e7:43:be'


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
