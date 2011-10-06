#! /usr/bin/env python

"""Reducers for distributed Map/Reduce.

This module contains code for both level 1 and level 2 reducers; see their
respective main functions for more details.
"""

import logging
import pickle
import re
import socket
import sys

from AppDesign.util import netutils


HELP = """Usage:
reducer.py 1 <mapper ip address> <mapper port> <reducer port>
reducer.py 2 <reducer 1 address> <reducer 1 port> <reducer 2 address> ...
"""

OBJ_RE = re.compile(r'{"[a-zA-Z]*": [0-9]+}')

class Reducer(object):
    def __init__(self):
        self.vals = {}

    def reduce(self, mapping):
        """Combine values for the same key into one.

        Args:
        mapping - The mapping to reduce.
        """
        key, val = mapping
        if key in self.vals:
            self.vals[key] += val
        else:
            self.vals[key] = val
        
def parse_object(token):
    """Parse an object from text.

    Args:
    token - The text representation of the object.

    Returns:
    The object, reconstructed from text.
    """
    token = token.replace("{", "(")
    token = token.replace("}", ")")
    token = token.replace(":", ",")
    obj = eval(token)
    return obj

def get_next_object(buf):
    """Retrieve the next object from the buffer.

    Args:
    buf - The text buffer to read from.

    Returns:
    The next text object in the buffer, None if there isn't one.
    """
    match = OBJ_RE.match(buf)
    if match:
        return match.group(0)
    else:
        return None

def get_next_mapping(buf):
    """Retrieve the next mapping from the buffer.

    Args:
    buf - The text buffer to read from.

    Returns:
    A tuple (mapping, new_buf). Mapping may be None if no mapping was found, or
    it was incomplete. new_buf will be the contents of the buffer with the
    mapping removed.
    """
    obj_txt = get_next_object(buf)
    if obj_txt:
        new_buf = buf[len(obj_txt):]  # Cut out the part we just parsed.
        mapping = parse_object(obj_txt)
        return (mapping, new_buf)
    else:
        return (None, buf)
            
def receive_values(reducer, source):
    """Receive values from a network socket and reduce them.

    Args:
    reducer - A reducer object used to reduce the values.
    source - A network socket connected to a data source, usually a mapper.
    """
    logging.info("Receiving values from", source.getpeername())
    data = ""
    while True:
        data += source.recv(1024)
        mapping, data = get_next_mapping(data)
        while mapping:
            reducer.reduce(mapping)
            mapping, data = get_next_mapping(data)
        if data:
            if data[-1] == "\0":
                break

def send_values(reducer, sink):
    """Send reduced values out on a network socket.

    Args:
    reducer - A Reducer object.
    sink - A network socket connected to the output sink.
    """
    logging.info("Sending values to", sink.getpeername())
    for mapping in reducer.vals.iteritems():
        sink.sendall('{"%s": %d}' % mapping)
    sink.sendall("\0")
        
def level_one_main():
    """Main function for a level 1 reducer.

    A level 1 reducer receives data from either a mapper or another level 1
    reducer, and combines values which have the same key. When the reducer
    receives null ('\\0') in the input, it ends the reduction.
    """
    if len(sys.argv) < 5:
        print "Too few arguments."
        print HELP
    elif len(sys.argv) > 5:
        print "Too many arguments."
        print HELP
    else:
        # Parse command line arguments.
        source_ip = sys.argv[2]
        source_port = int(sys.argv[3])
        local_port = int(sys.argv[4])
        localhost = netutils.get_ip_addr()
        logging.info("Preparing for level 1 reduce on host", localhost)
        logging.info("Source:", source_ip, source_port)
        
        # Set up sockets for remote communications.
        source = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # Enable logging to file.
        logging.basicConfig(filename="reducer-%s.log" % localhost,
                            level=logging.DEBUG)

        # Bind to local address and listen for new connections (from srv_socket)
        logging.debug("Binding to local address %s.", localhost)
        srv_socket.bind((localhost, local_port))
        srv_socket.listen(0)
        
        # Accept the sink connection. Now we're ready to start reducing.
        (sink, sink_address) = srv_socket.accept()
        logging.info("Received sink connection from", sink_address)
        srv_socket.close()

        # Reduce!
        source.connect((source_ip, source_port))
        logging.info("Beginning reduce.")
        reducer = Reducer()
        receive_values(reducer, source)
        send_values(reducer, sink)

        # Clean up after.
        logging.info("Closing connections.")
        sink.close()
        source.close()
        
def level_two_main():
    """Main function for a level 2 reducer.

    A level 2 reducer will accumulate the reduced data from the level 1 reducers
    provided at the command line and write the combined data to a pickle file.
    """
    logging.info("Preparing for level 2 reduce.")
    outfile = sys.argv[2]
    logging.info("Output file:")
    reducer = Reducer()
    for index in range(3, len(sys.argv), 2):
        reduce_host = sys.argv[index]
        reduce_port = int(sys.argv[index+1])
        logging.info("Connecting to", reduce_host, reduce_port)
        source = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # As soon as we connect, we're going to start receiving data.
        source.connect((reduce_host, reduce_port))
        logging.info("Reducing.")
        receive_values(reducer, source)
        logging.info("Closing connection.")
        source.close()

    # Reduce completed. Write it out.
    outfile = open(outfile, "w")
    logging.info("Dumping pickle file.")
    pickle.dump(reducer.vals, outfile)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Too few arguments."
        print HELP
    else:
        if int(sys.argv[1]) == 1:
            level_one_main()
        elif int(sys.argv[1]) == 2:
            level_two_main()
