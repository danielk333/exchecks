#!/usr/bin/env python

import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
server_address = ('localhost', 10000)
print(f'starting up on {server_address[0]} port {server_address[1]}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

code = 'utf-8'

packet_size = 1
max_len = 256
run_server = True
timeout = 5.0
end_char = '\n'


def send_msg(msg, connection):
    msg += end_char
    connection.sendall(msg.encode(code))


while run_server:
    # Wait for a connection
    print(f'waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print(f'connection from {client_address}')
        t0 = time.time()
        dt = 0.0

        while dt < timeout:
            dt = time.time() - t0

            data = ''
            while len(data) < max_len:
                data_raw = connection.recv(packet_size)
                if data_raw == end_char.encode(code):
                    break
                elif len(data_raw) > 0:
                    data += data_raw.decode(code)
                else:
                    dt = time.time() - t0
                    if dt >= timeout:
                        break

            command = False

            if data == 'arm off':
                send_msg('Black Knight: "Tis but a scratch."', connection)
                command = True

            if data == 'exit':
                print('Client exiting')
                send_msg('c-exit', connection)
                break

            if data == 'shutdown':
                run_server = False
                send_msg('Shutting down server', connection)
                send_msg('c-exit', connection)
                break

            if not data:
                send_msg('no command received', connection)
            else:
                print(f'received "{data}"')
                t0 = time.time()

            if command:
                t0 = time.time()
            else:
                send_msg('command not found', connection)

    finally:
        # Clean up the connection
        connection.close()

print('closing server')
