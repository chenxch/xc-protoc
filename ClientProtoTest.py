from socket import *
import google.protobuf
import TransportMessage_pb2
import WeChatOnlineNoticeMessage_pb2
import traceback
import google.protobuf.any_pb2
import threading
import time

Id = 0


def HearBeatReq_bytes():
    global Id
    Id += 1
    transportMessage = TransportMessage_pb2.TransportMessage()  # 注意括号不要掉了，
    transportMessage.MsgType = 1010
    transportMessage.Id = Id
    transportMessage.AccessToken = "ac897dss"
    print('心跳包数据...Id=', Id)
    return transportMessage.SerializeToString()


def OnlineNotice_bytes():
    global Id
    Id += 1
    transportMessage = TransportMessage_pb2.TransportMessage()  # 注意括号不要掉了，
    transportMessage.MsgType = 1020
    transportMessage.Id = Id
    transportMessage.AccessToken = "ac897dss"

    weChatOnlineNotice = WeChatOnlineNoticeMessage_pb2.WeChatOnlineNoticeMessage()
    weChatOnlineNotice.WeChatId = "wxid_123456789"
    weChatOnlineNotice.WeChatNo = "qdj_cancle"
    weChatOnlineNotice.WeChatNick = "昵称001"
    weChatOnlineNotice.Country = "中国"
    print('上线通知...Id=', Id)
    transportMessage.Content.Pack(weChatOnlineNotice)

    return transportMessage.SerializeToString()


def thread_HearBeat(tcpCliSock):
    while True:
        time.sleep(10)
        hearBeat_data = HearBeatReq_bytes()
        byte_data = hearBeat_data
        byte_head = (len(byte_data)).to_bytes(4, byteorder='big')
        tcpCliSock.send(byte_head)
        tcpCliSock.send(byte_data)
        print('10秒定时发送心跳包...\r\n发送数据[0].退出；[1].心跳包；[2].上线通知>')


if __name__ == "__main__":

    HOST = '127.0.0.1'
    PORT = 18080
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    t_hearBeat = threading.Thread(target=thread_HearBeat, args=(tcpCliSock,))
    t_hearBeat.start()  # 启动心跳线程
    while True:
        server_response = tcpCliSock.recv(1024)
        print(str(server_response, "utf8"))
        data1 = input('发送数据[0].退出；[1].心跳包；[2].上线通知>')
        print('输入指令：', data1)
        if data1 == '0':
            break
        if data1 == '1':
            hearBeat_data = HearBeatReq_bytes()
            byte_data = hearBeat_data
            byte_head = (len(byte_data)).to_bytes(4, byteorder='big')
            tcpCliSock.send(byte_head)
            tcpCliSock.send(byte_data)
        if data1 == '2':
            onlineNotice_bytes = OnlineNotice_bytes()
            byte_data = onlineNotice_bytes
            byte_head = (len(byte_data)).to_bytes(4, byteorder='big')
            tcpCliSock.send(byte_head)
            tcpCliSock.send(byte_data)

    tcpCliSock.close()