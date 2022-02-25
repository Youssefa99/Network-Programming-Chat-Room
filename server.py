import threading
import socket

# Run server on Localhost port 8080
host = "127.0.0.1"
port = 8080


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Server is Listening...")


clients = []
usernames = []


# broadcast message to all users
def broadcast(message):
    for client in clients:
        client.send(message)


# handle client sending messages and disconnecting from the server
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} has left the chat!!'.encode('ascii'))
            usernames.remove(username)
            break


# handle client connecting to the server
def receive():
    while True:
        client, address = server.accept()
        print(f'{str(address)} has connected to the server!')

        client.send('User'.encode('ascii'))  # send a message to notify user that he needs to give a username
        username = client.recv(1024).decode('ascii')  # receive username
        usernames.append(username)
        clients.append(client)

        print(f'Client Username is {username}')
        broadcast(f'{username} has joined the chat!'.encode('ascii'))
        client.send(f'Connected to the Server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
