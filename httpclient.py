#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        parsed = urlparse(url)
        host = parsed.hostname
        port = parsed.port
        path = parsed.path
        #print "host: %s\n" % host
       #print "port: %s\n" % port
        #print "path: %s\n" % path
        if port == None:
           port = 80
        url = str(host)+"|"+str(port)+"|"+str(path)
        print "URL: %s\n" % url
        return url

    def connect(self, host, port):
        # use sockets! port 80 by default
        if port == None:
            port = 80
        #connect the client socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        return s

    def get_code(self, data):
        print '#in get_code'
        return None

    def get_headers(self,data):
        print '#in get_headers'
        return None

    def get_body(self, data):
        print '#in get_body'
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        print 'inget'
        code = 500
        body = ""
        url = self.get_host_port(url)
        url = url.split("|")
        host = url[0]
        port = url[1]
        path = url[2]
        print "host: %s\nport: %s\npath: %s\n" % (host,port,path)

        socket = self.connect(host, port)
        if socket != None:
            if args != None:
                form_data = urllib.urlencode(args)
                path += "?" + form_data

            request = "GET %s HTTP/1.1\r\n" \
                      "Host: %s\r\n" \
                      "Connection: close\r\n" \
                      "Accept: */*\r\n\r\n" % (path, host)

            try:
                socket.send(request)
            except Exception as e:
                print e
                socket.shutdown(socket.SHUT_RDWR)
                socket.close()

                return HTTPRequest(code, body)

            data = self.recvall(socket)

            #socket.shutdown(socket.SHUT_RDWR)
            socket.close()

            code = self.get_code(data)
            body = self.get_body(data)
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        print 'inpost'
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            print 'is post'
            return self.POST( url, args )
        else:
            print 'is get'
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        print 'len <=1'
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print 'ELSIF'
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print 'ELSE'
        print client.command( command, sys.argv[1] )    
