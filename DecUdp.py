# !/usr/bin/env python
# -*- coding: utf-8-*-
# pylint:disable=invalid-name

"""Here is import lib
"""
# this is server
import os
import threading
import socket
from threading import Lock

"""Declare variable
"""
datList = [];
mutex = Lock();

"""Create upd socket.
"""
def CreateUdpSocket(port):
    # SOCK_DGRAM used for UPD
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind port
    # ip is null, we can get all
    udp_socket.bind(('', port))

    # broadcast
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return udp_socket

"""Receive Data from client
"""
def ReceiveDat():
    print("receive data")

"""Decode Data
"""
def DecodeDat():
    print("decode data")

if __name__ == "__main__":
    # Tell user to give us a port number.
    port = input('please give me a port number: ')

    # Get udp socket.
    udp_socket = CreateUdpSocket(int(port))

    # this thread do for receiving data from client.
    recv_thread = threading.Thread(target=ReceiveDat)
    recv_thread.setDaemon(True)
    recv_thread.start()

    # this thread do for decoding data
    dec_thread = threading.Thread(target=DecodeDat)
    dec_thread.setDaemon(True)
    dec_thread.start()

    udp_socket.close()
