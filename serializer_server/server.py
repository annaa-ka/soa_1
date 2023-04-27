import socketserver
import threading
import os
import socket
import struct
import sys
from tool import *
import logging

def get_data():
    ser_time, deser_time, size = 0, 0, 0
    if (os.getenv('TYPE') == 'NATIVE'):
        ser_time, deser_time, size = native_format()
    elif (os.getenv('TYPE') == 'JSON'):
        ser_time, deser_time, size = json_format()
    elif (os.getenv('TYPE') == 'XML'):
        ser_time, deser_time, size = xml_format()
    elif (os.getenv('TYPE') == 'GOOGLE_BUFFER'):
        ser_time, deser_time, size = protobuf_format()
    elif (os.getenv('TYPE') == 'APACHE'):
        ser_time, deser_time, size = apache_avro()
    elif (os.getenv('TYPE') == 'YAML'):
        ser_time, deser_time, size = yaml_test()
    elif (os.getenv('TYPE') == 'MESSAGEPACK'):
        ser_time, deser_time, size = msg_pack_test()
    data_to_send = os.getenv('TYPE') + '-'+ str(size) + '-' + str(int(ser_time*1000)) + 'ms' + '-' + str(int(deser_time*1000))+ 'ms'
    return data_to_send

# https://pymotw.com/2/socket/multicast.html
class MultiCastSocket():
    def __init__(self):
        self.multicast_group = os.getenv('MULTICAST_ADRESS')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.initialize()

    def initialize(self):
        proxy_address = ('', int(os.getenv('MULTICAST_PORT')))
        self.socket.bind(proxy_address)
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.multicast_group) + socket.inet_aton('0.0.0.0'))

    def receive_respond_loop(self):
        while True:
            _, address = self.socket.recvfrom(1024)
            data = get_data()
            self.socket.sendto(bytes(data + "\n", "utf-8"), address)

class UDPSocket():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host, port = os.getenv('TYPE'), int(os.getenv('PORT'))
        self.listening_address = (host, port)
        self.socket.bind(self.listening_address)

    def receive_respond_loop(self):
        while(True):
            _, address = self.socket.recvfrom(1024)
            data = get_data()
            self.socket.sendto(bytes(data + "\n", "utf-8"), address)

if __name__ == "__main__":
    launchme = UDPSocket()
    launchme2 = MultiCastSocket()
    t1 = threading.Thread(target=launchme.receive_respond_loop)
    t2 = threading.Thread(target=launchme2.receive_respond_loop)
    for t in [t1, t2]: t.start()
    for t in [t1, t2]: t.join()
