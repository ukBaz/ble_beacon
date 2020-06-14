============================
Workshop - Bluetooth Beacons
============================

Overview
========

Bluetooth Beacons are small devices that are transmit only devices. They send
small amounts of data that can be used for a number of applications.
How often a beacon transmits and the range of a beacon will vary depending on
the application it is being used for. The less frequently a beacon transmits
will mean it will use less power. As will turning the power down and reducing
the range. A typical beacon might transmit once a second and have a range
of 50 metres (line of sight) or one wall.

Applications
------------

Navigation
~~~~~~~~~~

Indoor navigation can be done with Bluetooth beacons. Think about it like a
lighthouse. The beacon will broadcast a message that is unique to it in the
same that the lighthouse's lights display with specific characteristic.
For example, the lighthouse at Cromer, Norfok has the characteristic of one
flash every minute and had a range of 27 miles.

For a Bluetooth Beacon this could be used to tell your phone that you are
in a particular room of a museum so an app on the phone could display
relevant information.

Tracking
~~~~~~~~

By attaching a Bluetooth beacon to an item of interest, because of the limited
range of Bluetooth, if the scanner can receive the signal it must mean the
beacon is close by.

This is a similar idea to how air traffic control monitors which aircraft are
close by.

Bluetooth Beacon technology was used for creating Tracking and Tracing Apps
without giving away peoples personal information.
It has also been used to track where equipment is in large builds. For example,
knowing which room a bed is in.

Formats
-------

A Bluetooth beacon used a part of the Bluetooth specification that allows devices
to advertise themselves. In most devices where you want to connect to them
they give information such as their name and services that they offer.

For a beacon there is upto 21 bytes to send information.
Different beacons use that space in different ways.


+---------------+--------------------+------------+
| Format        | Data Blocks        | Bytes used |
+===============+====================+============+
| iBeacon       | Beacon UUID        | 16         |
|               +--------------------+------------+
|               | Major              | 2          |
|               +--------------------+------------+
|               | Minor              | 2          |
|               +--------------------+------------+
|               | Transmit Power     | 1          |
+---------------+--------------------+------------+
| AltBeacon     | Beacon UUID        | 16         |
|               +--------------------+------------+
|               | Major              | 2          |
|               +--------------------+------------+
|               | Minor              | 2          |
|               +--------------------+------------+
|               | Transmit Power     | 1          |
+---------------+--------------------+------------+
| Eddystone UID | Transmit Power     | 1          |
|               +--------------------+------------+
|               | Namespace ID       | 10         |
|               +--------------------+------------+
|               | Instance ID        | 6          |
+---------------+--------------------+------------+
| Eddystone URL | Transmit Power     | 1          |
|               +--------------------+------------+
|               | URL encoded prefix | 1          |
|               +--------------------+------------+
|               | (Encoded) URL      | 17 (max)   |
+---------------+--------------------+------------+
| Exposure      | Rolling Proximity  | 16         |
| Notification  | Identifier         |            |
|               +--------------------+------------+
|               | Version Information| 1          |
|               +--------------------+------------+
|               | Transmit Power     | 1          |
+---------------+--------------------+------------+

Challenge 1
===========

Use the following code to answer these Questions:

    - How many beacons does the scanner find?
    - Are they all transmitting at the same power?
    - Which one do you think is closest to the scanner?

.. code-block:: python
   :linenos:

    from scanner import protocols, hci_socket

    for pkt in hci_socket.run():
        ad = protocols.AdvertEventHandler(pkt)
        if ad.eddystone_url:
            print(f'Found: {ad.eddystone_url.url}'
                  f' \u2191{ad.eddystone_url.tx_pwr} \u2193{ad.rssi}')

Challenge 2
===========

In the previous challenge we used Eddystone URL beacons that broadcast
a web address. For this challenge we are going to find Eddystone UID
which broadcast two numbers. One of those numbers is called "Instance ID"
and one is called "Namespace ID".

For the "Instance ID" of 11 (or 0x0b in hex), can you find the following:

   - How many beacons does the scanner find?
   - If we "decode" the Namespace ID", what word does it show?
   - What do all the words have in common?

Here is a clue how to decode the Namespace ID:

.. code-block:: python

   print(f'word: {ad.eddystone_uid.namespace_id.decode("utf-8")}')

Challenge 3
===========

We are going to use Eddystone UID beacons again for this challenge. However,
we are looking for beacons with the Instance ID value of 187 (0xbb)

There are hidden words in this challenge again, but this time rather than
using UTF-8 encoding directly, they have also encoded with base85.

For the "Instance ID" of 187 (or 0xbb in hex), can you find the following:

   - How many beacons does the scanner find?
   - If we "decode" the Namespace ID", what word does it show?
   - What do all the words have in common?

Here is a clude on how to decode the Namespace ID with base85:

.. code-block:: python

        if ad.eddystone_uid.instance_id == 0xbb:
            namespace_bytes = ad.eddystone_uid.data_in[1:11]
            hidden_word = base64.b85decode(namespace_bytes).decode("utf-8")