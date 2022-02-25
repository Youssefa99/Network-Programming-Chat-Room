import socket
import threading

username = input("Choose a Username:")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))


# handles messages sent to user
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'User':  # checks if server wants to know user's username
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            print("Connection Error")
            client.close()
            break


# handles messages sent from the user
def write():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
