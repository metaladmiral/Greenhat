from . import help, connect_to_client, get_targets


class Pre_Client_Cmd_Controller:

    def help():
        help.help()

    def connect_to_client(self_, client_uid):
        connect_to_client.connect_to_client(self_, client_uid)

    def get_targets(self_):
        get_targets.get_targets(self_)
