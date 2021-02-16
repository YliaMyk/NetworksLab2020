import socket
import sys
from threading import Thread
from datetime import datetime

host = 'localhost'
port = 6666
block_size = 1024
login_user = ''


def time():
    time_hour = str(datetime.now().time().hour)
    time_minute = str(datetime.now().time().minute)
    current_time = time_hour + ':' + time_minute

    return current_time


def creation_sock():
    global sock
    global login_user

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        login_user = input("Введите ваш логин: ")
        Thread(target=sending_messages).start()
        Thread(target=accepting_messages).start()
    except ConnectionRefusedError:
        print("Приносим свои извинения, неудалось подключиться к серверу Т-Т")
        sys.exit(1)


def sending_messages():
    global sock

    while True:
        message = f"[{login_user}]: {input()}".encode("utf-8")
        try:
            sock.send(message)
        except ConnectionResetError:
            print("Приносим свои извинения, сервер сейчас недоступен Т-Т")
            sys.exit(1)


def accepting_messages():
    global sock

    while True:
        try:
            message = sock.recv(block_size).decode("utf-8")
            print("<" + time() + ">" + message)

        except ConnectionResetError:
            print("Приносим свои извинения, сервер сейчас недоступен Т-Т")
            sys.exit(1)


def main():
    creation_sock()


if __name__ == '__main__':
    main()
