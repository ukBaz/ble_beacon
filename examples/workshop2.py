from scanner import protocols, hci_socket


for pkt in hci_socket.run():
    ad = protocols.AdvertEventHandler(pkt)
    if ad.eddystone_uid:
        print(f'instance id: {ad.eddystone_uid.instance_id}')
        if ad.eddystone_uid.instance_id == 11:
            print(f'namespace id: {ad.eddystone_uid.namespace_id}')
            word = ad.eddystone_uid.data_in
            print(f'word: {word}')
            print(f'word: {word[1:11].decode("utf-8")}')
