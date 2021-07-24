import socket
import tkinter as tk

from json import dumps, loads
from threading import Thread
from os import system, name
from time import sleep


system("")


def clear():
    system("cls" if name == 'nt' else "clear")


host, port = 'localhost', 8500

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



class Colors:
    
    def print(self, color, text) -> str:
        return "\033[38;2;{}m{}\033[38;2;255;255;255m".format(color, text)

    def red(self, text) -> str:
        return self.print('255;0;0', text)

    def green(self, text) -> str:
        return self.print('0;255;0', text)

    def blue(self, text) -> str:
        return self.print('0;0;255', text)



class Client:

    def __init__(self, socket):

        main_thread = Thread(target=self.tkinter)
        main_thread.start()

        window = tk.Tk()
        self.window = window

        window.title("Chat")

        geometry = self.tkinter_screen_set(400, 300)
        
        window.geometry(geometry)
        window.resizable(width=False, height=False)
        window.configure(background="black")


        self.var = var = tk.StringVar()
        var.set("Connexion au serveur en cours...")

        self.main_label = main_label = tk.Label(window, textvariable=var)


        main_label.pack()
        self.window.mainloop()

    def tkinter(self):


        while True:
            try:
                socket.connect((host, port))
            except ConnectionRefusedError:
                self.var.set("Erreur lors de la connexion au serveur. Tentative de reconnexionen cours...")
                continue
            break

        self.var.set("Récupération de l'identifiant...")

        self.socket = socket
        id = socket.recv(1024).decode('utf-8')

        self.id = id





        if not id:
            self.var.set("Le serveur est hors ligne. Réessayez plus tard.")
            disconnect_button = tk.Button(self.window(), text="Quitter", command=self.tkinter_exit_button).pack()
            input()

        
        self.var.set("Votre ID est: {}".format(id))

        sleep(2.5)

        self.window.title("Chat - ID: {}".format(id))
        
        self.set_username()

        self.connect()


    def set_username(self):
        self.username = None

        self.var.set("Entrez votre pseudo:")

        self.username_entry = username_entry = tk.Entry(self.window)
        username_button = tk.Button(self.window, text="Confirmer", command=self.tkinter_username_button)
        
        username_entry.pack()
        username_button.pack()

        while True:
            if self.username is not None:
                break

        username_button.pack_forget()

        self.var.set("Votre pseudo est: {}".format(self.username))

        sleep(2.5)

        self.window.title("Chat - ID: {} - Pseudo: {}".format(self.id, self.username))

        data = {'name':self.username}
        self.send(data)


    def connect(self):


        self.connected = None

        self.var.set("Entrez l'ID de l'utilisateur auquel vous voulez vous connecter:")

        self.connect_button = connect_button = tk.Button(self.window, text="Se connecter", command=self.tkinter_connect_button)
        connect_button.pack()

        while True:
            if self.connected is not None:
                break


        self.var.set(self.connected)

        if self.connected == "Waiting for connection...":
            self.username_entry.pack_forget()
            connect_button.pack_forget()
            while True:
                resp = self.socket.recv(1024).decode('utf-8')
                if resp:
                    self.var.set(resp)
                    break
        
        if self.username_entry.winfo_ismapped() and connect_button.winfo_ismapped():
            self.username_entry.pack_forget()
            connect_button.pack_forget()



        self.tkinter_chat()



    def tkinter_chat(self):

        self.window.geometry("1200x800")

        self.tkinter_chat_entry()

        self.tkinter_chat_button()

        recv_thread = Thread(target=self.tkinter_chat_recv)

        recv_thread.start()

        recv_thread.join()



    def send(self, data):
        try:
            self.socket.send(dumps(data).encode('utf-8'))
        except:
            return self.disconnect()


    def disconnect(self):
        try:
            self.socket.disconnect()
        except:
            pass
        return exit()
    

    def tkinter_chat_entry(self):
        text = tk.Entry(self.window)
        self.text = text

        text.pack(expand=True)
    
    def tkinter_chat_button(self):
        button = tk.Button(self.window, text="Envoyer", command=self.tkinter_chat_send)
        self.button = button
        
        button.pack(expand=True)

    def tkinter_chat_send(self):
        content = self.text.get()

        if content == "":
            return

        data = {'message':content}

        try:
            self.send(data)
        except:
            return self.disconnect()

        self.text.delete(first=0, last=len(self.text.get()))

        self.var.set(self.var.get() + '\n' + "{}: {}".format(self.username, content))

    def tkinter_chat_recv(self):
        while True:
            try:
                data = loads(socket.recv(1024).decode('utf-8'))
            except:
                return self.disconnect()

            for username in data['message']:
                self.var.set(self.var.get() + '\n' + username + ": " + data['message'][username])
                break
        
    
    def tkinter_username_button(self):
        username = self.username_entry.get()

        self.username_entry.delete(first=0, last=len(self.username_entry.get()))

        if len(username) < 3:
            self.var.set("Pseudo trop court! (min. 3)")
        
        elif len(username) > 10:
            self.var.set("Pseudo trop long! (max. 10)")
        
        else:
            self.username = username
    
    def tkinter_connect_button(self):
        content = self.username_entry.get()

        self.username_entry.delete(first=0, last=len(self.username_entry.get()))

        if content == self.id:
            self.connectino_error(
                "Tu ne peux pas te connecter à toi même xD"
            )

        data = {'connect':content}
        self.send(data)

        response = self.socket.recv(1024).decode('utf-8')

        if response == 'invalid id':
            self.connectino_error("ID invalide!")
        else:
            self.var.set(response)
            self.connected = response

    def connectino_error(self, text):
        self.var.set(text)
        self.username_entry.pack_forget()
        self.connect_button.pack_forget()
        disconnect_button = tk.Button(self.window(), text="Quitter", command=self.tkinter_exit_button).pack()
        input()




    def tkinter_screen_set(self, window_x, window_y):
        screen_x, screen_y = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        
        x = screen_x / 2 + window_x / 2
        y = screen_y / 2 + window_y / 2

        return "{}x{}+{}+{}".format(window_x, window_y, int(x), int(y))

    def tkinter_exit_button(self):
        return self.disconnect()



def main():


    client = Client(socket)


    socket.close()


if __name__ == '__main__':
    main()
