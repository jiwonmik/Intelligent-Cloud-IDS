#!/usr/bin/env python3

import socket
import json

# 접속할 서버 주소
HOST = 'X.X.X.X'
# 서버에서 지정해 놓은 포트 번호
PORT = 30000

try: 
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
except socket.error as err:
	print(“Error : %s”%(err))

server_socket.listen()
client_socket, addr = server_socket.accept()

Print(“Connected by”, addr)
b=b’’
while True:
	data = client_socket.recv(1024)
	b += data
	host = json.oads(b.decode(‘utf-8’))
	
	if not data:
		break
	
	client_ip = host[“public_ip”]
	print(“Received from”, addr, host)
	with open(‘/home/ec2-user/test_proj/iplist.json’, “a+”) as ip_list:
		for line in ip_list:
			if client_ip in ip_list:
				ip_list.close()
			else:
				ip_list.write(json.dumps(host, indent=”\t”))
				ip_list.write(“\n”)
				ip_list.close()
	client_socket.sendall(data)

client_socket.close()
server_socket.close()
