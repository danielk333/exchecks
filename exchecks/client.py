#!/usr/bin/env python

'''
Send arbitrary string to TCP/IP channel and get something back

'''

import socket
import sys
import multiprocessing as mp
import time

if len(sys.argv) > 1:
    raw_host = sys.argv[1]
    raw_host = raw_host.split(':')
    host = raw_host[0]
    port = int(raw_host[1])

else:
    port = 10000
    host = 'localhost'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (host, port)
print(f'connecting to {server_address[0]} port {server_address[1]}')

sock.connect(server_address)

code = 'utf-8'

# exit_command = 'close'
exit_command = 'exit'

packet_size = 1
max_len = 1024*100
end_char = '\n'


def receive(ret, sock):
    while True:
        data = ''
        while len(data) < max_len:
            data_raw = sock.recv(packet_size)
            if data_raw == end_char.encode(code):
                break
            elif len(data_raw) > 0:
                data += data_raw.decode(code)

        if data == 'c-exit':
            print('receive: Stopping client now...')
            break
        if len(data) > 0:
            ret.put(data)


def process_return(ret):
    while True:
        data = ret.get()
        if data is None:
            print('process_return: Stopping client now...')
            break
        if data == 'error':
            print('Something went wrong?')
        print(f'RETURN: {data}')
        # do more with returned data


def send_command_loop(out, ret, sock):
    try:
        cmd = ''
        while True:
            data = input()
            data += '\n'
            cmd += data

            sock.sendall(data.encode(code))

            if data.find(end_char) != -1:
                print(f'command sequence sent to server:\n "{cmd}"\n')
                if cmd == exit_command+end_char or cmd == 'shutdown'+end_char:
                    print('send_command_loop: Stopping client now...')
                    ret.put(None)
                    break
                cmd = ''

    finally:
        print('Closing socket')
        sock.close()


out = mp.Queue()
ret = mp.Queue()

# create queue to wait for command and listen to command and worker to execute results
ps = []

p_rec = mp.Process(target=receive, args=(ret, sock,))
ps.append(p_rec)
p_rec.start()

p_ret = mp.Process(target=process_return, args=(ret,))
ps.append(p_ret)
p_ret.start()

send_command_loop(out, ret, sock)

p_rec.terminate()
time.sleep(0.2)

for p in ps:
    p.join()

out.close()
ret.close()
