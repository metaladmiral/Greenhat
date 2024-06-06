import time
import constants


def check_conn(self_):
    while True:
        if self_.is_conn_established == False:
            time.sleep(5)
            continue
        try:
            for client_uid, client in self_.conn_list.items():
                try:
                    client.send(constants.CONN_CHECK_STRING.encode())
                except:
                    del self_.conn_list[client_uid]
                    del self_.client_details[client_uid]
                    self_.default_text = constants.DEFAULT_TEXT
                    print(
                        "\nCurrent Client has been disconnected!\nPress Enter to Continue\n"
                    )
        except:
            continue

        time.sleep(2)
