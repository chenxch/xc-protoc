import socket
import time
import google.protobuf
import google.protobuf.any_pb2
import TransportMessage_pb2
import WeChatOnlineNoticeMessage_pb2
import threading
import gevent
from gevent import socket, monkey

monkey.patch_all()
import socketserver

all_clients = []

class Myserver(socketserver.BaseRequestHandler):

    def handle(self):
        if (self.request) not in all_clients:
            all_clients.append(self.request)
        conn = self.request
        Thread_recv(conn)


def Thread_recv(socket_Server):
    try:
        while True:
            Head_data = socket_Server.recv(4)  # 接收数据头 4个字节,
            data_len = int.from_bytes(Head_data, byteorder='big')

            protobufdata = socket_Server.recv(data_len)

            tmessage = TransportMessage_pb2.TransportMessage()
            tmessage.ParseFromString(protobufdata)
            i_id = tmessage.Id
            i_msgtype = tmessage.MsgType
            now_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print(now_time, ' id:', i_id, 'msgType:', i_msgtype)
            if i_msgtype == 0:
                print('异常')
                break
            if i_msgtype == 1010:
                print(now_time, ' 服务器接收到心跳包...')
            if i_msgtype == 1020:
                print(now_time, ' 服务器接收到上线通知...')
                # 有上线通知，将好友信息和socket_Server套接字存放在buf中，
                # 这样可以将好友A的信息转发给好友B，做成及时聊天工具
                # 有下线通知，将好友信息和socket_Server套接字从buf中去掉
                # 服务器端功能就是收集上线和下线通知，转发聊天消息
                online = WeChatOnlineNoticeMessage_pb2.WeChatOnlineNoticeMessage()
                tmessage.Content.Unpack(online)
                print(now_time, ' WeChatNo:' + online.WeChatNo, 'WeChatId:' + online.WeChatId,
                      'WeChatNick:' + online.WeChatNick)
            server_response = input(">>>")
            # socket_Server.sendall(bytes(server_response, "utf8"))
            for clients in all_clients:
                if clients != socket_Server:
                    clients.send(bytes(server_response, "utf8"))
    # except expression as identifier:
    #     print('Thread_recv 异常...')
    finally:
        socket_Server.close()


if __name__ == "__main__":
    # 方法3
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 18080), Myserver)
    server.serve_forever()

    """s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    HostPort = ('192.168.0.100',11087)
    s.bind(HostPort)  #绑定地址端口
    s.listen(100)  #监听最多100个连接请求
    while True:
        print('server socket waiting...')

        obj,addr = s.accept()  #阻塞等待链接
        print('socket object:',obj)
        print('client info:',addr)

        #方法1
        #t_recv = threading.Thread(target=Thread_recv,args=(obj,))
        #t_recv.start()

        #方法2
        gevent.spawn(Thread_recv,obj)"""