import socket
import threading
import time


def tcp_link(sock, addr):
    # print('Accept new connection from %s ...' % addr)
    print(f'Accept new connection from {addr} ...')
    sock.send('Hello, Python!'.encode('utf-8'))
    while True:
        data = sock.recv(1024)
        print(data.decode('utf-8'))
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(("receive: %s" % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print(f'Connection from {addr} closed.')


def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 1314
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        sock, addr = server_socket.accept()
        t = threading.Thread(target=tcp_link, args=(sock, addr))
        t.start()


def main():
    socket_server()


if __name__ == '__main__':
    main()
