# ble_beacon
## STEM workshop reading bluetooth beacons
### Overview of aims
Bluetooth Smart (BLE) beacons are getting good press coverage with the likes of Apple's iBeacon, Gimbal and Google support of uriBeacon (Physical Web) so it would be good to take this technology and show that it is accessable to students and the maker community.

This is a work-in-progress project that is exploring at how to make this technology accessable to schools for STEM projects.
The assumption is that the workshop will leverage the Raspberry Pi hardware for doing coding involved in the workshop. Some assumptions being made at this time are:
* The RPi's will be the scanners
* The RPi's will be static
* The beacons will move
* The beacons will be based on an open standard
* All hardware will be commercially available (or could be substituded for commercially available hardware)
* The workshop code will allow for it to be easily extentable so students could do 'real' projects based on it (i.e. [go4SET](http://www.ukesf.org/working-with-schools/go4set-project)
* Use a language familiar to schools. This seems to be python although javascript (node.js) may be an option.

## Install bluetooth software on Raspberry Pi
### Older documentation seems to suggest:
There seems to be many different tutorials that seem to suggest many different packages need to be installed.
```
sudo apt-get install bluetooth bluez-utils blueman bluez-hcidump
```
### New document seems to suggest:
```
sudo apt-get install bluez python-gobject python-dbus
```
and maybe:
```
sudo apt-get install bluez-utils
```
It seems like this is important:
```
sudo apt-get install python-bluez
```
# Physical Web examples
To run the Linux example using Bluez then a newer version of awk needs to be installed. This can be done with:

```
sudo apt-get install gawk
```
# Useful references:

[ubuntu documentation](https://help.ubuntu.com/community/BluetoothSetup)

BlueZ 5 [API](http://www.bluez.org/bluez-5-api-introduction-and-porting-guide/)

### Python Examples of BlueZ
[BlueZ/test](https://github.com/aguedes/bluez/tree/master/test)

### This looks useful:

### Open Beacon Specs:
[AltBeacon Protocol Specification v1.0](https://github.com/AltBeacon/spec)

[UriBeacon Specification](https://github.com/google/uribeacon/tree/master/specification)

### Articles
[Beacon tracking with Node.js and Raspberry Pi](https://medium.com/@eklimcz/beacon-tracking-with-node-js-and-raspberry-pi-794afa880318)

[iBeacon Raspberry Pi Scanner in Python](http://www.switchdoc.com/2014/08/ibeacon-raspberry-pi-scanner-python/)

[iBeacons™ aren’t the only Fruit!](http://devblog.blackberry.com/2014/09/ibeacons-not-the-only-fruit/)

[Beacon introduction](http://www.slideshare.net/Dusan_Writer/ibeacon-and-bluetooth-le-an-introduction)

[Coffee with a Googler: Chat with Scott Jenson about the Physical Web](https://www.youtube.com/watch?v=w8zkLGwzP_4)
