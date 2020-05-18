from scanner import protocols, hci_socket


for pkt in hci_socket.run():
    ad = protocols.AdvertEventHandler(pkt)
    if ad.eddystone_uid:
        print(f'Raw packet: {pkt}')
        print(f'Clean hex values: {protocols._format_bytearray(pkt)}')
        print(f'Processed Eddystone UID: {ad.eddystone_uid.namespace_id}')
