"""Module to retrieve BLE advertising information from HCI socket"""
import socket
import struct
from time import sleep
from pydbus import SystemBus

bus = SystemBus()
adapter = bus.get('org.bluez', '/org/bluez/hci0')

LE_META_EVENT = 0x3E
HCI_EVENT_PKT = 0x04
EVT_CMD_COMPLETE = 0x0e
EVT_CMD_STATUS = 0x0f
EVT_LE_META_EVENT = 0x3e


def filter_on_le_evt():
    """Build bytes to configure HCI socket filter"""
    type_mask = 1 << HCI_EVENT_PKT
    event_mask1 = (1 << EVT_CMD_COMPLETE) | (1 << EVT_CMD_STATUS)
    event_mask2 = 1 << (EVT_LE_META_EVENT - 32)
    opcode = 0

    return struct.pack("<LLLH", type_mask, event_mask1, event_mask2, opcode)


def setup_socket():
    """Function to configure HCI socket to only show BLE advert events"""
    sock = socket.socket(
        socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
    sock.bind((0, ))
    sock.setsockopt(socket.SOL_HCI, socket.HCI_FILTER, filter_on_le_evt())
    sock.setblocking(0)
    return sock


def run():
    """Generator method to yield HCI Advertising packets"""
    sock = setup_socket()
    # Start discovery
    if not adapter.Discovering:
        adapter.StartDiscovery()

    try:
        while True:
            try:
                yield sock.recv(255)
            except BlockingIOError:
                sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        print('Cleaning up...')
        sock.close()
        adapter.StopDiscovery()
