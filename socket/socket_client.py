import socket
import time


def socket_client():
    # 创建socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    # print(host,type(host))
    port = 1314
    s.connect((host, port))
    print(s.recv(1024).decode('utf-8'))
    for data in ['小明','xiaozhi','xiaoqiang']:
        time.sleep(2)
        s.send(data.encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
    s.send(b'exit')
    s.close()


def main():
    socket_client()


if __name__ == '__main__':
    main()