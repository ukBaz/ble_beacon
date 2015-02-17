__author__ = 'barry'
import subprocess

cmd = './ble_dump.sh'
print cmd
ble_reader = subprocess.Popen(cmd,
                              shell=True,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              )
while 1:
    reply = ble_reader.stdout.readline()
    if reply != '':
        print('{0}'.format(reply))
