#! /usr/bin/env python
"""Mapper functions for a distributed Map/Reduce framework."""

import logging
import socket
import string
import sys
from AppDesign.util import netutils

__author__ = "Nick Pascucci (npascut1@gmail.com)"

HELP = """Usage:
mapper.py <source address> <source port> <mapper port>
"""

def tokenize(inputs):
    """Convert a string into a set of tokens.

    Args:
    inputs - A string to be tokenized.

    Returns:
    A list of lowercase words extraced from the string with all punctuation
    stripped.
    """
    tokens = inputs.lower().strip()
    tokens = tokens.translate(string.maketrans("",""), string.punctuation)
    tokens = tokens.replace("\0", "")
    tokens = tokens.split()
    return tokens

def map_token(token):
    """Apply a mapping function to the token.

    Args:
    token - The token to be mapped.

    Returns:
    A tuple (key, value)
    """
    return (token, 1)

def execute(source, sink):
    """Execute the map by reading from the source and writing to the sink.

    This function reads until a null byte is encountered. Each string read
    from the source is tokenized and mapped. The result is then sent to the
    sink. Output is valid JSON data, and may be parsed by a number of
    languages.

    Args:
    source - A socket connected to a data source.
    sink - A socket connected to a reducer.
    """
    logging.info("Executing Map.")
    while True:
        data = source.recv(1024)
        tokens = tokenize(data)
        for token in tokens:
            mapping = map_token(token)
            sink.sendall('{"%s": %d}' % mapping)
        if data[-1] == "\0":
            break
    sink.sendall("\0")

def main():
    if len(sys.argv) < 4:
        print "Too few arguments."
        print HELP
    elif len(sys.argv) > 4:
        print "Too many arguments."
        print HELP
    else:
        # Parse command line arguments.
        source_ip = sys.argv[1]
        source_port = int(sys.argv[2])
        local_port = int(sys.argv[3])

        # Set up sockets for remote communications.
        source = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        localhost = netutils.get_ip_addr()

        # Enable logging to file.
        logging.basicConfig(filename="mapper-%s.log" % localhost,
                            level=logging.DEBUG)

        # Bind to local address and listen for new connections (from srv_socket)
        logging.debug("Binding to local address %s.", localhost)
        srv_socket.bind((localhost, local_port))
        srv_socket.listen(0)
        
        # Accept the sink connection. Now we're ready to start mapping.
        (sink, sink_address) = srv_socket.accept()
        srv_socket.close()

        # Map!
        source.connect((source_ip, source_port))
        execute(source, sink)

        # Clean up after.
        sink.close()
        source.close()

    
if __name__ == "__main__":
    main()
