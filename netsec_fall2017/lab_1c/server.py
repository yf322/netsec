from netsec_fall2017.lab1_b.loginUsername import LogInWithUsername
from netsec_fall2017.lab1_b.loginStatus import LogInStatus
from netsec_fall2017.lab1_b.getUserProfile import GetUserProfleWithID
from netsec_fall2017.lab1_b.sendUserProfile import SendUserProfile
from asyncio.protocols import Protocol
from playground.network.packet import PacketType

class ServerProtocol(Protocol):

    def __init__(self):
        self.transport = None
        self.userID = None


    def connection_made(self, transport):
        print("Server Connected to Client")
        self.transport = transport
        self._deserializer = PacketType.Deserializer()

    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, LogInWithUsername):
                loginStatus = LogInStatus()
                print(pkt.password)
                if pkt.username != None or pkt.password != None:
                    loginStatus.status = True
                    loginStatus.userID = self.getUserIDWithName(pkt.username)
                else:
                    loginStatus.status = False
                    loginStatus.userID = None
                self.transport.write(loginStatus.__serialize__())

            elif isinstance(pkt, GetUserProfleWithID):
                sendUserProfile = SendUserProfile()
                sendUserProfile.profile = self.getUserProfileWithID("1")
                self.transport.write(sendUserProfile.__serialize__())


    def connection_lost(self, exc):
        self.transport = None
        print("Server Connection Lost Becasue {}".format(exc))

    def getUserIDWithName(self, username):
        return "1234"

    def getUserProfileWithID(self, userID):
        return '{"username": "Yongqiang Fan", "userID": "1"}'
