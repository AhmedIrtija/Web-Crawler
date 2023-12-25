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


def query(ips, timeout=10):
    startTime = time.time()
    #create a packet
    query = struct.pack('!H', 1234)
    query += struct.pack('!H', 0)
    query += struct.pack('!H', 1)
    query += struct.pack('!H', 0)
    query += struct.pack('!H', 0)
    query += struct.pack('!H', 0)

    for t in tmz.split('.'):
        query += struct.pack('B', len(t))
        query += struct.pack('!{}s'.format(len(t)), t.encode('utf-8'))

    query += struct.pack('B', 0)
    query += struct.pack('!H', 1)
    query += struct.pack('!H', 1)


    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.settimeout(timeout)

    try:
        for ip in ips:
            udp.sendto(query, (ip, 53))

        
            response = udp.recvfrom(512)[0]
            elapsed_time = time.time() - startTime

            print(f"Received response for {ip} in {elapsed_time:.2f} seconds")
            print(f"Successful for {ip}")

            udp.close()
            return response
        
    except socket.timeout:
        print(f"Timeout for {ip}")


def httpRequest(ips):
    for ip in ips:
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.settimeout(10)

            startTime = time.time()
            tcp.connect((ip, 80))
            connectionTime = time.time()

            http_request = b"GET / HTTP/1.1\r\nHost: " + tmz.encode('utf-8') + b"\r\n\r\n"
            tcp.sendall(http_request)

            http_response = tcp.recv(4096)
            endTime = time.time()

            dnsRtt = connectionTime - startTime
            httpRtt = endTime - connectionTime

            print(f'Printing for {ip} with the response - {http_response}\n\n')
            print(f"DNS RTT to {ip}: {dnsRtt:.4f} seconds")
            print(f"HTTP RTT to {ip}: {httpRtt:.4f} seconds")
            print(f"Total RTT to {ip}: {(dnsRtt + httpRtt):.4f} seconds\n")

        except socket.error as e:
            print(f"Error while connecting to {ip}: {e}")

        finally:
            tcp.close()


def printInfo(type, rtt, ans, add):
    print(f'RTT for {type} - {rtt:.3}')
    print(f'Answers for {type}- {ans}')
    print(f'Additionals for {type} - {add}')



#DNS Request to the Root
startTime = time.time()
response = query(root_records)
endTime = time.time()
RTT1 = endTime - startTime
answers, additionals = unpack(response)
printInfo("Root", RTT1, answers, additionals)


#DNS Request to the TLD
startTime = time.time()
response = query(additionals)
endTime = time.time()
RTT2 = endTime - startTime
answers, additionals = unpack(response)
printInfo("TLD", RTT2, answers, additionals)


#DNS Request to the Authoritative
startTime = time.time()
response = query(additionals)
endTime = time.time()
RTT3 = endTime - startTime
answers, additionals = unpack(response)
printInfo("Authoritative", RTT3, answers, additionals)

rttDNS = RTT1 + RTT2 + RTT3
print(f'DNS Resolver RTT - {rttDNS:.3}')

#HTTP Request
startTime = time.time()
httpRequest(answers)
endTime = time.time()
RTT4 = endTime - startTime
print(f'HTTP Request RTT - {RTT4:.3}')
