from scanner import protocols, hci_socket
import base64

for pkt in hci_socket.run():
    ad = protocols.AdvertEventHandler(pkt)
    if ad.eddystone_uid:
        print(f'\nBeacon instance id: {ad.eddystone_uid.instance_id}'
              f' @ ({ad.address[-5:]})')
        if ad.eddystone_uid.instance_id == 0xbb:
            namespace_bytes = ad.eddystone_uid.data_in[1:11]
            hidden_word = base64.b85decode(namespace_bytes).decode("utf-8")
            print(f'Namespace Value:\t{ad.eddystone_uid.namespace_id}')
            print(f'Namespace Bytes:\t{namespace_bytes}')
            print(f'Hidden word:    \t{hidden_word}')
