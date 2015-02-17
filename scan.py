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
    reply = ble_reader.stdout.readline().rstrip()
    if reply != '':
        print('{0}'.format(reply))
        my_tuple = [int(x, 16) for x in reply.split()]
        print len(my_tuple)