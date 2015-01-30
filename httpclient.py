#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle, Brian Trinh
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
        parsed = urlparse(url) #parses URL
        host = parsed.hostname #gets hostname
        port = parsed.port     #gets port
        path = parsed.path     #gets path
        if port == None:
           port = 80           #sets 80 as default
        url = str(host)+"|"+str(port)+"|"+str(path)
        return url

    def connect(self, host, port):
        if port == None:
            port = 80          #sets 80 as default
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        return s

    def get_code(self, data):
        code = int(data.split()[1])
        return code

    def get_headers(self,data): #is this even used?
        header = data.split("\r\n\r\n")[0]
        return header

    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body

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
        code = 500
        body = ""
        url = self.get_host_port(url)
        url = url.split("|") #splits on | added earlier 
        host = url[0]
        port = url[1]
        path = url[2]

        socket = self.connect(host, port)
        if socket != None:
            if args != None:
                params = urllib.urlencode(args) # encodes args

            request = "GET %s HTTP/1.1\r\n" \
                      "Host: %s\r\n" \
                      "Connection: close\r\n" \
                      "Accept: */*\r\n\r\n" % (path, host)

            try:
                print'%s' % request
                socket.send(request)
            except Exception as e:
                print e
                socket.close()

            data = self.recvall(socket)

        return HTTPRequest(self.get_code(data), self.get_body(data))

    def POST(self, url, args=None):
        code = 500
        body = ""
        url = self.get_host_port(url)
        url = url.split("|")
        host = url[0]
        port = url[1]
        path = url[2]
        #print "host: %s\nport: %s\npath: %s\n" % (host,port,path)

        socket = self.connect(host, port)
        if socket != None:

            if args == None:
                length = 0 
                newpath = ""                    # if no argument make length 1. may not need newpath
            else:
                params = urllib.urlencode(args) #encodes args
                length = len(params)            #gets content length

        request = "POST %s HTTP/1.1\r\n" \
                  "Host: %s\r\n" \
                  "Connection: close\r\n" \
                  "Content-Type: application/x-www-form-urlencoded\r\n" \
                  "Accept: */*\r\n" \
                  "Content-Length: %s\r\n\r\n" % (path, host, str(length))
        #print "REQUEST:: %s" % request

        if args != None:
            request += params

        try:
            print'%s' % request
            socket.send(request)
        except Exception as e:
            print e
            socket.close()

        data = self.recvall(socket)

        return HTTPRequest(self.get_code(data), self.get_body(data))

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
