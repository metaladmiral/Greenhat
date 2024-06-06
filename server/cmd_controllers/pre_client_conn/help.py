import constants


def help():
    print("All the current supported commands - \n")
    for i, cmds in enumerate(constants.PRE_CONN_CMDS):
        print(str(i) + ".", str(cmds), "-", constants.PRE_CONN_CMDS[cmds])
