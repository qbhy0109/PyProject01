import socket
import time


def socket_client():
    # 创建socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = 'www.baidu.com'
    host = 'yjzq.online'
    port = 80
    s.connect((host, port))
    time.sleep(2)
    s.send('GET / HTTP/1.1\r\nHost:yjzq.online\r\nConnection:close\r\n\r\n'.encode('utf-8'))
    buffer = []
    while True:
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break
    data = b''.join(buffer)

    header, html = data.split(b'\r\n\r\n', 1)
    print(header.decode('utf-8'))

    with open('yjzq.html','wb') as f:
        f.write(html)
    s.close()


def main():
    socket_client()


if __name__ == '__main__':
    main()