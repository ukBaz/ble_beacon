"""
Example that prints out complete raw packets from HCI event and also
just the raw advertising data payload from a device.
"""
from scanner import protocols, hci_socket


for pkt in hci_socket.run():
    print(f'\nraw: {pkt}')
    print(f'packet as list: {protocols.format_bytearray(pkt)}')
    ad = protocols.AdvertEventHandler(pkt)
    if ad.adv_data:
        print(f'\tRaw Advert payload ({ad.address}): {ad.adv_data}')
