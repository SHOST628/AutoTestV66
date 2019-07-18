import socket


def main():
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    dest_addr = ("127.0.0.1", 5678)
    bind_addr = ("",8080)
    udp_socket.bind(bind_addr)
    while True:
        send_msg = input("please input message to send: ")
        if send_msg == "quit":
            break
        udp_socket.sendto(send_msg.encode("utf-8"), dest_addr)
        recv_msg = udp_socket.recvfrom(1024)
        print("msg: %s  from %s" % (recv_msg[0].decode("utf-8"), str(recv_msg[1])))
    udp_socket.close()

if __name__ == '__main__':
    main()

