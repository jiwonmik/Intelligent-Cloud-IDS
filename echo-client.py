#!/usr/bin/env python3

import socket
from requests import get
import json
import netifaces as ni

HOST = 'X.X.X.X'
PORT = 30000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

hostname=socket.gethostbyaddr(socket.gethostname())[0]
public_ip=get('https://api.ipify.org').text
ni.ifaddresses('eth0')
private_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

host = dict(zip(['hostname', 'public_ip', 'private_ip'], [hostname, public_ip, private_ip]))

client_socket.sendall(json.dumps(host).encode('utf-8'))

data = client_socket.recv(1024)
print('Received: ', repr(data.decode()))

client_socket.close()
