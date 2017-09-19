from myPackets import *
from asyncio.protocols import Protocol
from playground.network.packet import PacketType
from passThrough import *
from playground.network.common import StackingTransport, StackingProtocolFactory, StackingProtocol
import asyncio
import playground
import logging

class ServerProtocol(Protocol):

    def __init__(self):
        self.transport = None
        self.state = 0


    def connection_made(self, transport):
        print("Server Connected to Client")
        self.transport = transport
        self._deserializer = PacketType.Deserializer()


    def data_received(self, data):

        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            print(pkt)
            if isinstance(pkt, LogInWithUsername) and self.state == 0:
                loginStatus = LogInStatus()
                print(pkt.password)
                if pkt.username != None or pkt.password != None:
                    loginStatus.status = True
                    loginStatus.userID = self.getUserIDWithName(pkt.username)
                else:
                    loginStatus.status = False
                    loginStatus.userID = None
                self.state += 1
                self.transport.write(loginStatus.__serialize__())

            elif isinstance(pkt, GetUserProfleWithID) and self.state == 1:
                sendUserProfile = SendUserProfile()
                sendUserProfile.profile = self.getUserProfileWithID("1")
                self.transport.write(sendUserProfile.__serialize__())

            else:
                self.transport.close()
                print("Error packet from client")
                #sys.exit(2)


    def connection_lost(self, exc):
        self.transport = None
        print("Server Connection Lost Becasue {}".format(exc))

    def getUserIDWithName(self, username):
        return "1234"

    def getUserProfileWithID(self, userID):
        return '{"username": "Yongqiang Fan", "userID": "1"}'


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    f = StackingProtocolFactory(lambda: PassThrough1(), lambda: PassThrough2())
    ptConnector = playground.Connector(protocolStack=f)
    playground.setConnector("passThrough", ptConnector)

    logging.getLogger().setLevel(logging.NOTSET)
    logging.getLogger().addHandler(logging.StreamHandler())

    coro = playground.getConnector("passThrough").create_playground_server(lambda: ServerProtocol(), 8080)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
