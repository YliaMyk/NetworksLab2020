import socket
import time
from threading import Thread


users = []
len_сhar = 8  # количество байт для кодирования количества символов в строке
len_name = 10  # максимальный размер логина
len_sec = 16  # количество байт для кодирования секунд
ip = '127.0.0.1'
port = 7777


def creation_sock():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen()
    print("Старт сервера")

    while True:
        user_sock, user_ip = server_socket.accept()
        Thread(target=new_connection, args=(user_sock, user_ip, )).start()


def current_time(sec):
    current_time = time.strftime('%H:%M', time.localtime(sec))
    return current_time


def new_connection(user_sock, user_ip):
    users.append(user_sock)
    print(f"К нам подключился новый юзер {user_ip[0]}:{user_ip[1]}")
    accept_and_send_a_message(user_sock, user_ip)


def check_length(socket, content, length):
    while len(content) < length:
        content += socket.recv(length - len(content))
        if length == len(content):
            break


def get_message(user_sock):
    while True:
        try:
            header = user_sock.recv(len_сhar + len_name)
        except Exception:
            return

        if not header:
            return

        check_length(user_sock, header, len_сhar + len_name)

        header = header.decode('utf-8')
        header_len_char = header[:len_сhar]

        try:
            int(header_len_char)
        except ValueError:
            continue

        header_len_char = int(header_len_char)
        header_name = header[len_сhar:].strip()

        message = user_sock.recv(header_len_char)

        check_length(user_sock, message, header_len_char)

        message = message.decode('utf-8')

        return {"len": header_len_char, "name": header_name, "time": message}


def accept_and_send_a_message(user_sock, user_ip):

    while True:
        message = get_message(user_sock)
        sec = int(time.time())
        server_formatted_time = current_time(sec)

        if not message:
            user_sock.shutdown(socket.SHUT_WR)
            user_sock.close()
            print(f"Пользователь отключился {user_ip[0]}:{user_ip[1]}")
            users.remove(user_sock)
            return

        print(f"Получено {message['name']} {server_formatted_time}: {message['time']}")
        header_to_send = f"{message['len']:<{len_сhar}}{message['name']:<{len_name}}{sec:<{len_sec}}"
        message_to_send = header_to_send + message['time']
        message_to_send = message_to_send.encode('utf-8')

        for user in users:
            if user != user_sock:
                try:
                    user.send(message_to_send)
                except Exception:
                    user.close()
                    users.remove(user)
                    continue


def main():
    creation_sock()


if __name__ == '__main__':
    main()

