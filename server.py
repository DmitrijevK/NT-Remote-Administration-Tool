import os
import platform
import argparse
import socket
import uuid
import pymysql.cursors

# Connect to the database
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="",
  database="cv2test"
)
mycursor = mydb.cursor()


def console_command(client, command):
    client.send(command.encode())
    output = client.recv(1024).decode()
    print(output)

def remove_device(ip_address):
    sql = "DELETE FROM cv WHERE Ipaddress = %s"
    mycursor.execute(sql, (ip_address,))
    mydb.commit()
    print("Device with IP address %s has been removed from the database.")

def check_unique_device(ip_address):
    sql = "SELECT * FROM cv WHERE Ipaddress = %s"
    mycursor.execute(sql, (ip_address,))
    result = mycursor.fetchone()
    if result:
        return True
    else:
        return False

def send_command(ip_address, command):
    if check_unique_device(ip_address):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip_address, 5000))
        console_command(client, command)
        client.close()
    else:
        print("Device with IP address %s is not found in the database." % (ip_address))

def send_command_for_all(command):
    sql = "SELECT Ipaddress FROM cv"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        send_command(row[0], command)
    else:
        print("This device is not registered in the database")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 5000
sock.bind((host, port))
sock.listen()
print("Server started on %s:%s" % (host, port))



while True:
    client, address = sock.accept()
    print("Received a new connection from %s:%s" % (address[0], address[1]))
    sql = "INSERT INTO cv (Mac, Ipaddress, OS, Provider) VALUES (%s, %s, %s, %s)"
    val = (uuid.getnode(), address[0], platform.system(), "Provider")
    mycursor.execute(sql, val)
    mydb.commit()
    
    #Handler
    while True:
        command = input("Enter command: ")
        if command == "exit":
            break
        elif command == "/remove":
            remove_device(address[0])
        elif command == "/for_all":
            command_all = input("Enter command for all clients: ")
            send_command_for_all(command_all)
        else:
            send_command(address[0], command)

client.close()
mycursor.close()
mydb.close()
