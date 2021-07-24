import socket

from threading import Thread
from json import dumps
from random import randint

from src.client import Client, clients


host, port = '', 8500



socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


socket.bind((host, port))
print("Le serveur est en ligne!")



def client_start(conn, addr, surplus=0):

    client_number = randint(100, 1000) + surplus


    if client_number in clients:
        return client_start(conn, addr, client_number)

    return client_thread_start(conn, addr, client_number)



def client_thread_start(conn, addr, client_number):

    try:
        conn.send(str(client_number).encode('utf-8'))
        Client(client_number, conn, addr)
    except:
        pass
    
    return client_number




def listen():
    socket.listen()
    conn, addr = socket.accept()

    client_start(conn, addr)
    return listen()


def stop_loop():
    stop = input("")
    if stop == 'y':
        socket.close()
        
    return stop_loop()





loop = Thread(target=listen)
stop_thread = Thread(target=stop_loop)

loop.start()
stop_thread.start()



loop.join()



for client in clients:
    client.close()

socket.close()

