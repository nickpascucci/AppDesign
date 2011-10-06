#! /usr/bin/env python

import logging
import re
import socket
import sys

from AppDesign.util import netutils


HELP = """Usage:
reducer.py <mapper ip address> <mapper port> <reducer port>
"""

obj_re = re.compile(r'{"[a-zA-Z]*": [0-9]+}')

class Reducer(object):
    def __init__(self):
        self.vals = {}

    def reduce(self, mapping):
        key, val = mapping
        if key in self.vals:
            self.vals[key] += val
        else:
            self.vals[key] = val
        
def parse_object(token):
    token = token.replace("{", "(")
    token = token.replace("}", ")")
    token = token.replace(":", ",")
    obj = eval(token)
    return obj

def get_next_object(buf):
    match = obj_re.match(buf)
    if match:
        return match.group(0)
    else:
        return None

def get_next_mapping(buf):
    obj_txt = get_next_object(buf)
    if obj_txt:
        new_buf = buf[len(obj_txt):]  # Cut out the part we just parsed.
        mapping = parse_object(obj_txt)
        return (mapping, new_buf)
    else:
        return (None, buf)
            
def execute(source, sink):
    reducer = Reducer()
    data = ""
    while True:
        data += source.recv(1024)
        print "Data:", data
        mapping, data = get_next_mapping(data)
        while mapping:
            print "Got mapping:", mapping
            reducer.reduce(mapping)
            mapping, data = get_next_mapping(data)
        if data[-1] == "\0":
            break
    for mapping in reducer.vals.iteritems():
        sink.send('{"%s": %d}' % mapping)
    sink.send("\0")
        
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
        logging.basicConfig(filename="reducer-%s.log" % localhost,
                            level=logging.DEBUG)

        # Bind to local address and listen for new connections (from srv_socket)
        logging.debug("Binding to local address %s." % localhost)
        srv_socket.bind((localhost, local_port))
        srv_socket.listen(0)
        
        # Accept the sink connection. Now we're ready to start reducing.
        (sink, sink_address) = srv_socket.accept()
        srv_socket.shutdown(socket.SHUT_RDWR)
        srv_socket.close()

        # Reduce!
        source.connect((source_ip, source_port))
        execute(source, sink)

        # Clean up after.
        sink.shutdown(socket.SHUT_RDWR)
        source.shutdown(socket.SHUT_RDWR)
        sink.close()
        source.close()
        
            
if __name__ == "__main__":
    main()
