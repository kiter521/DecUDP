# !/usr/bin/env python
# -*- coding: utf-8-*-
# pylint:disable=invalid-name

"""Here is import lib
"""
# this is server
import os
import threading
import socket
import time, datetime
from threading import Lock

"""Declare variable
"""
datList = [];
mutex = Lock();

HEADER_ADDR = 11;
VENDER_ADDR = 2;
VENDER_ID = 0x4857;
STA_HEAD = 15;
TLV_TIME_STAMP_START = 17;
TLV_TIME_STAMP_END = 20;

"""Other fields we do not care now.(Ex. version...)
"""

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
def ReceiveDat(udp_socket):
    print("receive data")
    while True:
        data = udp_socket.recvfrom(1024)
        mutex.acquire()
        datList.append(data)
        mutex.release()

"""Decode Data
"""
def DecodeDat(udp_socket):
    print("decode data")
    while True:
        mutex.acquire()
        tmpDat = datList.pop(0)
        mutex.release()
        ###0:UDP data 1:ip info, so we use 0 index.
        tmpDat = tmpDat[0]
        ###decode tmpDat
        dat_size = len(tmpDat)
        header_info = tmpDat[0:HEADER_ADDR]
        vender_info = header_info[0:VENDER_ADDR]
        ###make sure,this data begin with 0x4857
        if vender_info != VENDER_ID:
            continue
        sta_info = tmpDat[HEADER_ADDR + 1:dat_size]
        ###deal with STA data
        tmp_len = len(sta_info)
        if tmp_len < 14:
            continue

        while tmp_len > 0:
            sta_flag = sta_info[13] and 0x01
            ###if sta flag is 0, means no TLV data, we should deal next sta data
            if sta_flag != 1:
                sta_info = sta_info[STA_HEAD + 1:tmp_len]
                tmp_len = len(sta_info)
                continue
            ###sta flag is 1, means there has TLV data
            ###deal with TLV data
            option_len = sta_info[STA_HEAD + 1]
            ###according optionlength,we can get TLVs
            ###but now we only get first TLV's time stamp.
            time_stamp = sta_info[TLV_TIME_STAMP_START:TLV_TIME_STAMP_END]
            str_time_stamp = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time_stamp))
            print("first TLV time is :%s", str_time_stamp)
            ### here we can continue get other TLV, but now, we skip
            ### TODO
            ### we get next STA info
            sta_info = sta_info[STA_HEAD + option_len + 1 : tmp_len]
            tmp_len = len(sta_info)

if __name__ == "__main__":
    # Tell user to give us a port number.
    port = input('please give me a port number: ')

    # Get udp socket.
    udp_socket = CreateUdpSocket(int(port))

    # this thread do for receiving data from client.
    recv_thread = threading.Thread(target=ReceiveDat, args=(udp_socket,))
    recv_thread.setDaemon(True)
    recv_thread.start()

    # this thread do for decoding data
    dec_thread = threading.Thread(target=DecodeDat, args=(udp_socket,))
    dec_thread.setDaemon(True)
    dec_thread.start()

    udp_socket.close()
