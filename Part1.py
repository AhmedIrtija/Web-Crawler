import socket 
import struct
import time


tmz = "tmz.com"

root_records = []
#All the root records from the provided website from a - m
root_records.append("198.41.0.4")
root_records.append("199.9.14.201")
root_records.append("192.33.4.12")
root_records.append("199.7.91.13")
root_records.append("192.203.230.10")
root_records.append("192.5.5.241")
root_records.append("192.112.36.4")
root_records.append("198.97.190.53")
root_records.append("192.36.148.17")
root_records.append("192.58.128.30")
root_records.append("193.0.14.129")
root_records.append("199.7.83.42")
root_records.append("202.12.27.33")


def unpack(response):
    offset = 12
    IPServers = []
    ipAdd = []

    _, _, questions, answer, authority, additional = struct.unpack('!6H', response[:12])
    #unpack the headers to use them 
    for _ in range(questions):
            while response[offset] != 0:
                offset += 1

            offset += 5
    
    for _ in range(answer):
        if response[offset] >= 192: 
            offset += 2  
        else:
            while response[offset] != 0:
                offset += 1
            offset += 1  

        type_, _, _, data_length = struct.unpack('!HHIH', response[offset:offset + 10])
        offset += 10  

        if type_ == 1:  
            address = socket.inet_ntoa(response[offset:offset + data_length])
            ipAdd.append(address)

        elif type_ == 28:  
            address = socket.inet_ntop(socket.AF_INET6, response[offset:offset + data_length])
            ipAdd.append(address)

        offset += data_length  

    for _ in range(authority):
        if response[offset] >= 192: 
            offset += 2

        else:
            while response[offset] != 0:
                offset += 1
            offset += 1
        offset += 10  
        data_length = struct.unpack('!H', response[offset-2:offset])[0]
        offset += data_length  
    
    for _ in range(additional):
        if response[offset] >= 192: 
            offset += 2
        else:
            while response[offset] != 0:
                offset += 1
            offset += 1

        type_, _, _, data_length = struct.unpack('!HHIH', response[offset:offset+10])
        offset += 10
        if type_ == 1:  
            address = socket.inet_ntoa(response[offset:offset+4])
            offset += 4
            IPServers.append(address)
        else:
            offset += data_length

    return ipAdd, IPServers


