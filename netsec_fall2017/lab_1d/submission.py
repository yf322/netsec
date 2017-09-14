from myPackets import *
from myProtocols import *
import sys
import asyncio
import playground



USAGE = """usage: echotest <mode>
  mode is either 'server' or a server's address (client mode)"""

if __name__ == "__main__":
    echoArgs = {}

    args = sys.argv[1:]
    i = 0
    for arg in args:
        if arg.startswith("-"):
            k, v = arg.split("=")
            echoArgs[k] = v
        else:
            echoArgs[i] = arg
            i += 1

    if not 0 in echoArgs:
        sys.exit(USAGE)

    mode = echoArgs[0]
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)

    if mode.lower() == "server":
        coro = playground.getConnector().create_playground_server(lambda: ServerProtocol(), 101)
        server = loop.run_until_complete(coro)
        print("Echo Server Started at {}".format(server.sockets[0].gethostname()))
        loop.run_forever()
        loop.close()


    else:
        coro = playground.getConnector().create_playground_connection(lambda : ClientProtocol(), "20174.1.1.1", 101)
        transport, protocol = loop.run_until_complete(coro)
        print("Echo Client Connected. Starting UI t:{}. p:{}".format(transport, protocol))
        loginWithUsername = LogInWithUsername()
        getUserProfile = GetUserProfleWithID()
        protocol.loginStart(loginWithUsername, getUserProfile)
        loop.run_forever()
        loop.close()