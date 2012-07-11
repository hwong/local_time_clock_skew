import datetime
import random
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import sys
import time

EPOCH_1970_OFFSET = 2208988800L
NTP_PORT = 123

connection = socket(AF_INET, SOCK_DGRAM)

ntp_request = '\x1b' + 47 * '\0'

connection.sendto(ntp_request, ("%s.pool.ntp.org" % random.randint(0, 3), NTP_PORT))

ntp_response, address = connection.recvfrom(1024)

local_time = time.time()

if ntp_response:
    print "Response received from:", address[0]

    # http://tools.ietf.org/html/rfc2030
    ntp_packet = struct.unpack('!12I', ntp_response)

    transmit_timestamp_seconds = ntp_packet[10]
    transmit_timestamp_seconds -= EPOCH_1970_OFFSET
    transmit_timestamp_fraction = ntp_packet[11]

    ntp_time = float("%s.%s" % (transmit_timestamp_seconds, transmit_timestamp_fraction))

    skew = ntp_time - local_time

    print "ntp:\t %s" % ntp_time
    print "local:\t %s" % local_time
    print "skew:\t%s%s" % ("-" if skew >= 0 else "+", abs(skew))
else:
    print "No data received."

