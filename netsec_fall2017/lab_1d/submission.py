from myPackets import *
from myProtocols import *
import sys
import asyncio
import playground

#
# class EchoControl:
#     def __init__(self):
#         self.txProtocol = None
#
#     def buildProtocol(self):
#         return ClientProtocol(self.callback)
#
#     def connect(self, txProtocol):
#         self.txProtocol = txProtocol
#         print("Echo Connection to Server Established!")
#         self.txProtocol = txProtocol
#         sys.stdout.write("Enter Message: ")
#         sys.stdout.flush()
#         asyncio.get_event_loop().add_reader(sys.stdin, self.stdinAlert)
#
#     def callback(self, message):
#         print("Server Response: {}".format(message))
#         sys.stdout.write("\nEnter Message: ")
#         sys.stdout.flush()
#
#     def stdinAlert(self):
#         data = sys.stdin.readline()
#         if data and data[-1] == "\n":
#             data = data[:-1]  # strip off \n
#         self.txProtocol.send(data)


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
        remoteAddress = mode
        # control = EchoControl()
        coro = playground.getConnector().create_playground_connection(ClientProtocol(loop), "20174.1.1.1", 101)
        transport, protocol = loop.run_until_complete(coro)
        print("Echo Client Connected. Starting UI t:{}. p:{}".format(transport, protocol))
        loginWithUsername = LogInWithUsername()
        getUserProfile = GetUserProfleWithID()
        protocol.loginStart(loginWithUsername, getUserProfile)
        # control.connect(protocol)
        loop.run_forever()
        loop.close()