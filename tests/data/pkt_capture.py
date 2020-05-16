data = [
    b'\x04\x0e\x04\x01\x05 \x00',
    b'\x04\x0e\x04\x01\x0b \x00',
    b'\x04\x0e\x04\x01\x0c \x00',
    b'\x04>+\x02\x01\x03\x01\x97\xe7/s\x18b\x1f\x1e\xff\x06\x00\x01\t \x02[=cdI\xb9kQl\x977W\xc2V?\xa2k\xe7\x1c\xf4\x9d\xd7\x85\xc9',
    b'\x04>\x1a\x02\x01\x00\x01\x07\xbb\xd8!p\\\x0e\x02\x01\x06\n\xffL\x00\x10\x05\x0b\x1c\xfd\xf3\xc6\xad',
    b'\x04>\x0c\x02\x01\x04\x01\x07\xbb\xd8!p\\\x00\xae',
    b'\x04>\x1a\x02\x01\x00\x01\xd1e\xa9\x85\x0bI\x0e\x02\x01\x1a\n\xffL\x00\x10\x05\x03\x18\x9bF\x86\xa7',
    b'\x04>(\x02\x01\x02\x01\xc9\x9b1\xca\x82i\x1c\x1b\xff\xff\xff\xbe\xacH%>Yr$Dc\xb9\xb8\x03?\xfa\xb5\x81\x04\x00{\x01A\xbc\x00\xb2',
    b'\x04>\x0c\x02\x01\x04\x01\xc9\x9b1\xca\x82i\x00\xb3',
    b'\x04>\x1e\x02\x01\x00\x01\x1bQm\xb7Qd\x12\x02\x01\x1a\x02\n\x0c\x0b\xffL\x00\x10\x06\x03\x1e\xa0\xdeI?\xac',
    b'\x04>\x0c\x02\x01\x04\x01\x1bQm\xb7Qd\x00\xad',
    b"\x04>'\x02\x01\x02\x01\n\t9\x1b\xf6y\x1b\x1a\xffL\x00\x02\x15j\xb1|\x17\xf4{MA\x806Rj\xee\xd2/s\x01\x16\x03h\xbf\xb6",
    b'\x04>\x0c\x02\x01\x04\x01\n\t9\x1b\xf6y\x00\xb6',
    b"\x04>\x1f\x02\x01\x02\x01\x9c\xa0\xd0L'P\x13\x03\x03\xaa\xfe\x0e\x16\xaa\xfe\x10\xbd\x01firstuk\x01\xb4",
    b"\x04>\x0c\x02\x01\x04\x01\x9c\xa0\xd0L'P\x00\xb4",
    b'\x04>(\x02\x01\x02\x01\xb9\xf6\x0f\xfd\xe2\\\x1c\x03\x03\x9f\xfe\x17\x16\x9f\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xab',
    b'\x04>\x0c\x02\x01\x04\x01\xd1e\xa9\x85\x0bI\x00\xa8',
    b'\x04>\x16\x02\x01\x04\x01\xb9\xf6\x0f\xfd\xe2\\\n\t\xff\xe0\x00\x01z\xca\x86\xa1\xca\xaa',
    b'\x04>(\x02\x01\x03\x00k\xa0\xd0.\x04\xf8\x1c\x1b\xffu\x00B\x04\x01\x80\xac\xf8\x04.\xd0\xa0k\xfa\x04.\xd0\xa0j\x01\x17@\x00\x00\x00\x00\xa8',
    b'\x04>\x1a\x02\x01\x00\x01\xc7\xaf\x92\x15!b\x0e\x02\x01\x1a\n\xffL\x00\x10\x05\x13\x1c\x0c\xb2G\xa4',
    b'\x04>\x0c\x02\x01\x04\x01\xc7\xaf\x92\x15!b\x00\xa5',
    b'\x04\x0e\x04\x01\x0c \x00',
    b'\x04\x0f\x04\x00\x01\x01\x04',
    b'\x04\x0e\x04\x01\x05 \x00',
    b'\x04\x0e\x04\x01\x0b \x00',
    b'\x04\x0e\x04\x01\x0c \x00',
    b'\x04>+\x02\x01\x03\x01\x97\xe7/s\x18b\x1f\x1e\xff\x06\x00\x01\t \x02[=cdI\xb9kQl\x977W\xc2V?\xa2k\xe7\x1c\xf4\x9d\xd7\x85\xc9',
    b'\x04>(\x02\x01\x02\x01\xc9\x9b1\xca\x82i\x1c\x1b\xff\xff\xff\xbe\xacH%>Yr$Dc\xb9\xb8\x03?\xfa\xb5\x81\x04\x00{\x01A\xbc\x00\xb1',
    b'\x04>\x0c\x02\x01\x04\x01\xc9\x9b1\xca\x82i\x00\xb1',
    b'\x04>\x1a\x02\x01\x00\x01\xd1e\xa9\x85\x0bI\x0e\x02\x01\x1a\n\xffL\x00\x10\x05\x03\x18\x9bF\x86\xab',
    b'\x04>\x0c\x02\x01\x04\x01\xd1e\xa9\x85\x0bI\x00\xac',
    b'\x04>\x1e\x02\x01\x00\x01\x1bQm\xb7Qd\x12\x02\x01\x1a\x02\n\x0c\x0b\xffL\x00\x10\x06\x03\x1e\xa0\xdeI?\xae',
    b'\x04>\x0c\x02\x01\x04\x01\x1bQm\xb7Qd\x00\xac',
    b'\x04>(\x02\x01\x02\x01\xb9\xf6\x0f\xfd\xe2\\\x1c\x03\x03\x9f\xfe\x17\x16\x9f\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xaf',
    b'\x04>\x16\x02\x01\x04\x01\xb9\xf6\x0f\xfd\xe2\\\n\t\xff\xe0\x00\x01z\xca\x86\xa1\xca\xb0',
    b"\x04>\x1f\x02\x01\x02\x01\x9c\xa0\xd0L'P\x13\x03\x03\xaa\xfe\x0e\x16\xaa\xfe\x10\xbd\x01firstuk\x01\xb2",
    b"\x04>\x0c\x02\x01\x04\x01\x9c\xa0\xd0L'P\x00\xb1"
    b"\x04>'\x02\x01\x02\x01\n\t9\x1b\xf6y\x1b\x1a\xffL\x00\x02\x15j\xb1|\x17\xf4{MA\x806Rj\xee\xd2/s\x01\x16\x03h\xbf\xb6"
    b'\x04>\x0c\x02\x01\x04\x01\n\t9\x1b\xf6y\x00\xb5',
    b'\x04>\x1a\x02\x01\x00\x01\x07\xbb\xd8!p\\\x0e\x02\x01\x06\n\xffL\x00\x10\x05\x0b\x1c\xfd\xf3\xc6\xa8',
    b'\x04>)\x02\x01\x03\x01\xbeC\xe75\x82\xde\x1d\x02\x01\x06\x03\x03\xaa\xfe\x15\x16\xaa\xfe\x10\xf6\x03ukbaz.github.io\xbb',
    b'\x04>\x0c\x02\x01\x04\x01\x07\xbb\xd8!p\\\x00\xae',
]

beacon_only = [
    b"\x04>\x1f\x02\x01\x02\x01\x9c\xa0\xd0L'P\x13\x03\x03\xaa\xfe\x0e\x16\xaa\xfe\x10\xbd\x01firstuk\x01\xb4",
    b"\x04>\x1f\x02\x01\x02\x01\x9c\xa0\xd0L'P\x13\x03\x03\xaa\xfe\x0e\x16\xaa\xfe\x10\xbd\x01firstuk\x01\xb2",
    b'\x04>)\x02\x01\x03\x01\xbeC\xe75\x82\xde\x1d\x02\x01\x06\x03\x03\xaa\xfe\x15\x16\xaa\xfe\x10\xf6\x03ukbaz.github.io\xbd',
    b'\x04>)\x02\x01\x03\x01\xbeC\xe75\x82\xde\x1d\x02\x01\x06\x03\x03\xaa\xfe\x15\x16\xaa\xfe\x10\xf6\x03ukbaz.github.io\xbb',
    b"\x04>'\x02\x01\x02\x01\n\t9\x1b\xf6y\x1b\x1a\xffL\x00\x02\x15j\xb1|\x17\xf4{MA\x806Rj\xee\xd2/s\x01\x16\x03h\xbf\xb6",
    b"\x04>'\x02\x01\x02\x01\n\t9\x1b\xf6y\x1b\x1a\xffL\x00\x02\x15j\xb1|\x17\xf4{MA\x806Rj\xee\xd2/s\x01\x16\x03h\xbf\xb6",
    b'\x04>(\x02\x01\x02\x01\xc9\x9b1\xca\x82i\x1c\x1b\xff\xff\xff\xbe\xacH%>Yr$Dc\xb9\xb8\x03?\xfa\xb5\x81\x04\x00{\x01A\xbc\x00\xb2',
    b'\x04>(\x02\x01\x02\x01\xc9\x9b1\xca\x82i\x1c\x1b\xff\xff\xff\xbe\xacH%>Yr$Dc\xb9\xb8\x03?\xfa\xb5\x81\x04\x00{\x01A\xbc\x00\xb1',
]

bytes_only = [
    b'\x04\x3e\x1f\x02\x01\x02\x01\x9c\xa0\xd0\x4c\x27\x50\x13\x03\x03\xaa\xfe\x0e\x16\xaa\xfe\x10\xbd\x01\x66\x69\x72\x73\x74\x75\x6b\x01\xb4',
    b'\x04\x3e\x1f\x02\x01\x02\x01\x9c\xa0\xd0\x4c\x27\x50\x13\x03\x03\xaa\xfe\x0e\x16\xaa\xfe\x10\xbd\x01\x66\x69\x72\x73\x74\x75\x6b\x01\xb2',
    b'\x04\x3e\x29\x02\x01\x03\x01\xbe\x43\xe7\x35\x82\xde\x1d\x02\x01\x06\x03\x03\xaa\xfe\x15\x16\xaa\xfe\x10\xf6\x03\x75\x6b\x62\x61\x7a\x2e\x67\x69\x74\x68\x75\x62\x2e\x69\x6f\xbd',
    b'\x04\x3e\x29\x02\x01\x03\x01\xbe\x43\xe7\x35\x82\xde\x1d\x02\x01\x06\x03\x03\xaa\xfe\x15\x16\xaa\xfe\x10\xf6\x03\x75\x6b\x62\x61\x7a\x2e\x67\x69\x74\x68\x75\x62\x2e\x69\x6f\xbb',
    b'\x04\x3e\x27\x02\x01\x02\x01\x0a\x09\x39\x1b\xf6\x79\x1b\x1a\xff\x4c\x00\x02\x15\x6a\xb1\x7c\x17\xf4\x7b\x4d\x41\x80\x36\x52\x6a\xee\xd2\x2f\x73\x01\x16\x03\x68\xbf\xb6',
    b'\x04\x3e\x27\x02\x01\x02\x01\x0a\x09\x39\x1b\xf6\x79\x1b\x1a\xff\x4c\x00\x02\x15\x6a\xb1\x7c\x17\xf4\x7b\x4d\x41\x80\x36\x52\x6a\xee\xd2\x2f\x73\x01\x16\x03\x68\xbf\xb6',
    b'\x04\x3e\x28\x02\x01\x02\x01\xc9\x9b\x31\xca\x82\x69\x1c\x1b\xff\xff\xff\xbe\xac\x48\x25\x3e\x59\x72\x24\x44\x63\xb9\xb8\x03\x3f\xfa\xb5\x81\x04\x00\x7b\x01\x41\xbc\x00\xb2',
    b'\x04\x3e\x28\x02\x01\x02\x01\xc9\x9b\x31\xca\x82\x69\x1c\x1b\xff\xff\xff\xbe\xac\x48\x25\x3e\x59\x72\x24\x44\x63\xb9\xb8\x03\x3f\xfa\xb5\x81\x04\x00\x7b\x01\x41\xbc\x00\xb1',
]
