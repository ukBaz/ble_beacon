from scanner import protocols, hci_socket
import webbrowser

for pkt in hci_socket.run():
    ad = protocols.AdvertEventHandler(pkt)
    if ad.eddystone_url:
        print(f'Found: {ad.eddystone_url.url}'
              f' \u2191{ad.eddystone_url.tx_pwr} \u2193{ad.rssi}')
        webbrowser.open(ad.eddystone_url.url)
