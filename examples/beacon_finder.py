"""
Example of how to print information about beacons of interest
"""
from scanner import protocols, hci_socket


for pkt in hci_socket.run():
    ad = protocols.AdvertEventHandler(pkt)
    if ad.alt_beacon:
        print(f'\tAltBeacon: {ad.alt_beacon.beacon_uuid} @ {ad.rssi}dB')
    elif ad.ibeacon:
        print(f'\tiBeacon: [{ad.ibeacon.beacon_uuid}] '
              f'Major:{ad.ibeacon.major}  '
              f'Minor:{ad.ibeacon.minor} @ {ad.rssi}dB')
    elif ad.eddystone_url:
        print(f'\tEddystone-URL: {ad.eddystone_url.url} @ {ad.rssi}dB')
    elif ad.eddystone_uid:
        print(f'\tEddystone-UID: {ad.eddystone_uid.namespace_id}'
              f'-{ad.eddystone_uid.instance_id} @ {ad.rssi}dB')
