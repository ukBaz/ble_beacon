from scanner import protocols, hci_socket


for pkt in hci_socket.run():
    print(f'\nraw: {pkt}')
    print(f'packet as list: {protocols._format_bytearray(pkt)}')
    ad = protocols.AdvertEventHandler(pkt)
    if ad.adv_data:
        print(f'\tRaw Advert payload: {ad.adv_data}')