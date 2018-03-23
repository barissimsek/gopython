'''

SLOW HTTP POST ATTACK DETECTOR

Slow HTTP attacks are denial-of-service (DoS) attacks in which the attacker sends HTTP requests in pieces slowly, 
one at a time to a Web server. If an HTTP request is not complete, or if the transfer rate is very low, 
the server keeps its resources busy waiting for the rest of the data. When the server\'s concurrent connection pool
reaches its maximum, this creates a DoS. Slow HTTP attacks are easy to execute because they require only 
minimal resources from the attacker.

Ref: https://blog.qualys.com/securitylabs/2011/11/02/how-to-protect-against-slow-http-attacks

I used dpkt library to decode/parse the PCAP file

Baris Simsek, https://github.com/barissimsek

TODO: Needed to be tested with different pcaps.

'''

import datetime
import dpkt
import socket

HTTP_PORT = 80
MAX_TCP_PAYLOAD = 20
MIN_POST_SEGMENT = 20

def tcp_flags(flags):
    ret = ''
    if flags & dpkt.tcp.TH_FIN:
        ret = ret + 'F'
    if flags & dpkt.tcp.TH_SYN:
        ret = ret + 'S'
    if flags & dpkt.tcp.TH_RST:
        ret = ret + 'R'
    if flags & dpkt.tcp.TH_PUSH:
        ret = ret + 'P'
    if flags & dpkt.tcp.TH_ACK:
        ret = ret + 'A'
    if flags & dpkt.tcp.TH_URG:
        ret = ret + 'U'
    if flags & dpkt.tcp.TH_ECE:
        ret = ret + 'E'
    if flags & dpkt.tcp.TH_CWR:
        ret = ret + 'C'

    return ret

def parse_pcap_file():

    fd = open('./sample.pcap')
    pcap = dpkt.pcap.Reader(fd)
    conn = dict() # Store all connections with the respective 5tuple as index

    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)

        # Skip Non-IP ethernet packages
        if eth.type != dpkt.ethernet.ETH_TYPE_IP:
            continue

        # If it's an IP network
        ip = eth.data

        # Skip UDP packets
        if ip.p != dpkt.ip.IP_PROTO_TCP:
            continue

        tcp = ip.data

        # Check only defined inbound HTTP port
        if tcp.dport != HTTP_PORT:
            continue

        tf = tcp_flags(tcp.flags)

        # Create a new connection with the 5-tuples key
        tuple5 = (ip.dst, ip.src, tcp.dport, tcp.sport, ip.p)

        if tcp.data[:4] == 'POST':
            conn[tuple5] = {
                'isHttpPost': 1,
                'numberOfSegments': 0
                }
        elif tuple5 in conn and len(tcp.data) < MAX_TCP_PAYLOAD and tf == 'PA': 
        # Process only the segments have an initial POST request
            conn[tuple5] = {
                'isHttpPost': 1,
                'numberOfSegments': conn[tuple5]['numberOfSegments']+1
                }
        else:
            # Do not process those that don't have respected POST connection
            continue

    # Print Slow POST Attack connections only
    for k,v in conn.items():
        if v['numberOfSegments'] > MIN_POST_SEGMENT:
            print k, v

    fd.close()

if __name__ == '__main__':

    parse_pcap_file()






