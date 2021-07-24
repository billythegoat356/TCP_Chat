import socket

from random import randint
from threading import Thread
from json import dumps, loads


clients = {}



class Client:
    



    
    def __init__(self, id:int, conn, addr) -> None:


        clients[str(id)] = self

        self.id = str(id)
        self.conn = conn
        self.addr = addr
        
        self.name = None
        self.linked = None



        self.thread = Thread(target=self.connect)
        self.thread.start()



    def connect(self):
        

        try:
            data = loads(self.conn.recv(1024).decode('utf-8'))
            if len(data) > 1:
                return self.disconnect()
        except:
            return self.disconnect()


        
        thread = Thread(target=self.message_handler, args=[data])

        thread.start()

        return self.connect()

    
    def send(self, content):
        try:
            self.conn.send(content.encode('utf-8'))
        except:
            return




    def message_handler(self, data):

        if self.name is None:
            if 'name' in data and len(data['name']) < 10:
                self.name = data['name']
                print(f"{self.id} : {self.name}")
            else:
                self.disconnect()


        if 'connect' in data:
            if self.linked is not None:
                return self.disconnect()                           


            if data['connect'] not in clients or data['connect'] == self.id:
                self.send('invalid id')
                return self.disconnect()

            else:
                self.linked = clients[data['connect']]

                if self.linked.linked != self:
                    self.send('Waiting for connection...')
                    # self.linked.send('Someone connected to you! ID: {self.id}!')
                else:
                    self.send('Connected!')
                    self.linked.send("Connected!")

        elif 'message' in data:
            if not self.linked:
                self.send('invalid id')
                self.disconnect()
            if self.linked.linked == self:
                self.linked.send(dumps({'message':{self.name:data['message']}}))

    def disconnect(self):
        try:
            del clients[self.id]
            return self.conn.close()
        except:
            pass






class Admin(Client):
    pass