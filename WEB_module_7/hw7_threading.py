import socket
import threading
from time import sleep


def serv_func(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        client_id = 0
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        client_id += 1
        with conn:
            print(f'Connected by {addr}\n')
            while True:
                data = conn.recv(1028).decode()
                if not data:
                    conn.send(
                        f'FROM CLIENT {client_id} sent no more data.'.encode())
                    break
                elif data in ('stop', 'break', 'end', '.'):
                    conn.send(
                        f'FROM CLIENT {client_id} sent {data} to break connection.'.encode())
                    break
                print(f'FROM CLIENT {client_id}: {data}')
                conn.sendall(input('>>> ').encode())


def client_func(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((host, port))
        sleep(1)

        while True:
            s.sendall(input('>>> ').encode())
            data = s.recv(1028).decode()
            if data in ('stop', 'break', 'end', '.'):
                break
            print(f'FROM SERVER: {data}')


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 50001

    server = threading.Thread(target=serv_func, args=(HOST, PORT))
    client = threading.Thread(target=client_func, args=(HOST, PORT))

    server.start()
    client.start()

    server.join()
    client.join()
    print('DONE')
