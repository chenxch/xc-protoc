import time
import Message_pb2
from gevent import monkey

monkey.patch_all()
import socketserver

all_clients = []

def HearBeatReq_bytes(name,msg):
    result = Message_pb2.MessageResponse()  # 注意括号不要掉了，
    result.Name = name
    result.Msg = msg
    result.Code = 0
    result.Time = time.strftime('%Y-%m-%d %H:%M:%S')
    return result.SerializeToString()

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
            msgReq = Message_pb2.MessageRequest()
            msgReq.ParseFromString(protobufdata)
            code = msgReq.Code
            now_time = time.strftime('%Y-%m-%d %H:%M:%S')
            if code == 0:
                name = msgReq.Name
                msg = msgReq.Msg
                print(now_time, ' name:', name, 'msg:', msg)
                hearBeat_data = HearBeatReq_bytes(name,msg)
                byte_data = hearBeat_data
                byte_head = (len(byte_data)).to_bytes(4, byteorder='big')
                for clients in all_clients:
                    # if clients != socket_Server:
                    clients.send(byte_head)
                break
            if code == 200:
                print(now_time, ' 服务器接收到心跳包...')
            # server_response = input(">>>")
            # # socket_Server.sendall(bytes(server_response, "utf8"))
            # for clients in all_clients:
            #     if clients != socket_Server:
            #         clients.send(bytes(server_response, "utf8"))
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