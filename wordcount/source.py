#! /usr/bin/env python

import logging
import socket
import sys
from AppDesign.util import netutils

"""Simple source script for distributed Map/Reduce."""

HELP = """Usage:
source.py <filename> <port>
"""

def main():
    if len(sys.argv) < 3:
        print "Too few arguments."
        print HELP
    elif len(sys.argv) > 3:
        print "Too many arguments."
        print HELP
    else:
        # Parse command line args, open input file
        data_file = open(sys.argv[1], "r")
        local_port = int(sys.argv[2])

        # Open the server socket to accept connections
        srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        localhost = netutils.get_ip_addr()
        srv_socket.bind((localhost, local_port))
        srv_socket.listen(0)
        (sink, sink_address) = srv_socket.accept()

        # Now that we have someone listening, start talking.
        for line in data_file:
            sink.send(line)
        # End the data transmission.
        sink.send("\0")

        # Clean up.
        sink.shutdown(socket.SHUT_RDWR)
        sink.close()

if __name__ == "__main__":
    main()
