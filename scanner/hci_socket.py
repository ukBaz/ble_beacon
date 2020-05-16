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
    typeMask = 1 << HCI_EVENT_PKT
    eventMask1 = (1 << EVT_CMD_COMPLETE) | (1 << EVT_CMD_STATUS)
    eventMask2 = 1 << (EVT_LE_META_EVENT - 32)
    opcode = 0

    return struct.pack("<LLLH", typeMask, eventMask1, eventMask2, opcode)


def setup_socket():
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
    s.bind((0, ))
    s.setsockopt(socket.SOL_HCI, socket.HCI_FILTER, filter_on_le_evt())
    s.setblocking(0)
    return s


def run():
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

