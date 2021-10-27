import asynchat
import asyncore


# 定义端口
PORT = 6666

# 定义结束异常类
class EndSession(Exception):
    pass


class ChatServer(asyncore.dispatcher):
    """
    聊天服务器
    """

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        # 创建socket
        self.create_socket()
        # 设置 socket 为可重用
        self.set_reuse_addr()
        # 监听端口
        self.bind(('', port))
        self.listen(5)
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)


class ChatSession(asynchat.async_chat):
    """
    负责和客户端通信
    """

    def __init__(self, server, sock):
        asynchat.async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator(b'\n')
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))

    def enter(self, room):
        # 从当前房间移除自身，然后添加到指定房间
        try:
            cur = self.room
        except AttributeError:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        # 接收客户端的数据
        self.data.append(data.decode("utf-8"))

    def found_terminator(self):
        # 当客户端的一条数据结束时的处理
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line.encode("utf-8"))
        # 退出聊天室的处理
        except EndSession:
            self.handle_close()

    def handle_close(self):
        # 当 session 关闭时，将进入 LogoutRoom
        asynchat.async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))

class CommandHandler:
    """
    命令处理类
    """

    def unknown(self, session, cmd):
        # 响应未知命令
        # 通过 asynchat.async_chat.push 方法发送消息
        session.push(('Unknown command {} \n'.format(cmd)).encode("utf-8"))

    def handle(self, session, line):
        line = line.decode()
        # 命令处理
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        # 通过协议代码执行相应的方法
        method = getattr(self, 'do_' + cmd, None)
        try:
            method(session, line)
        except TypeError:
            self.unknown(session, cmd)











