from myPackets import *
from asyncio.protocols import Protocol
from playground.network.packet import PacketType
from passThrough import *
from playground.network.common import StackingTransport, StackingProtocolFactory, StackingProtocol
import asyncio
import playground
import logging

class ClientProtocol(Protocol):

    def __init__(self, loop):
        self.transport = None
        self.loop = loop
        self.state = 0

    def connection_made(self, transport):
        print("Connected to the server")
        self.transport = transport
        self._deserializer = PacketType.Deserializer()

    def data_received(self, data):

        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            print(pkt)
            if isinstance(pkt, LogInStatus) and self.state == 0:
                if pkt.status:
                    print("User request profile with ID: {}".format(pkt.userID))
                    self.getUserProfile.userID = pkt.userID
                    self.state += 1
                    self.transport.write(self.getUserProfile.__serialize__())
                else:
                    print("Login error, please check username or password")


            elif isinstance(pkt, SendUserProfile) and self.state == 1:
                print("The user profile is:\n {}".format(pkt.profile))

            else:
                self.transport.close()
                print("Error packet from server")
                #sys.exit(1)

    def connection_lost(self, exc):
        self.transport.close()
        print("Server Connection Lost Becasue {}".format(exc))
        self.loop.stop()

    def getUsernameInput(self):
        return "Yongqiang Fan"

    def getPasswordInput(self):
        return "123456"

    def loginStart(self, loginWithUsername, getUserProfile):
        self.loginWithUsername = loginWithUsername
        self.getUserProfile = getUserProfile
        loginWithUsername.username = self.getUsernameInput()
        loginWithUsername.password = self.getPasswordInput()
        print("User Logging in with username: {}".format(loginWithUsername.username))
        self.transport.write(loginWithUsername.__serialize__())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    f = StackingProtocolFactory(lambda : PassThrough1(), lambda : PassThrough2())
    ptConnector = playground.Connector(protocolStack=f)
    playground.setConnector("passThrough", ptConnector)

    logging.getLogger().setLevel(logging.NOTSET)
    logging.getLogger().addHandler(logging.StreamHandler())

    coro = playground.getConnector("passThrough").create_playground_connection(lambda: ClientProtocol(loop), '20174.1.1.1', 8080)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

