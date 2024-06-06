def get_targets(self_):
    print("Available computers - \n")
    for i, client_uid in enumerate(self_.client_details):
        print(
            str(i) + ".",
            str(self_.client_details[client_uid]["name"]),
            "-",
            str(client_uid),
        )

    print(
        "Use: \"connect clientid\" command to connect to that computer. Client ID is after the '-' above "
    )
