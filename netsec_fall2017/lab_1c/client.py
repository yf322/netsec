import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from netsec_fall2017.lab1_b.loginUsername import LogInWithUsername
from netsec_fall2017.lab1_b.loginStatus import LogInStatus
from netsec_fall2017.lab1_b.getUserProfile import GetUserProfleWithID
from netsec_fall2017.lab1_b.sendUserProfile import SendUserProfile
from asyncio.protocols import Protocol
from playground.network.packet import PacketType

class ClientProtocol(Protocol):

    def __init__(self, loop):
        self.transport = None
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        loginSession = LogInWithUsername()
        loginSession.username = self.getUsernameInput()
        loginSession.password = self.getPasswordInput()
        print("User Logging in with username: {}".format(loginSession.username))
        self.transport.write(loginSession.__serialize__())


    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, LogInStatus):
                getUserProfile = GetUserProfleWithID()
                if pkt.status:
                    print("User request profile with ID: {}".format(pkt.userID))
                    getUserProfile.userID = pkt.userID
                    self.transport.write(getUserProfile.__serialize__())
                else:
                    print("TODO Error message")

            if isinstance(pkt, SendUserProfile):
                print("The user profile\n {}".format(pkt.profile))

    def connection_lost(self, exc):
        self.transport = None
        print("Server Connection Lost Becasue {}".format(exc))

    def getUsernameInput(self):
        return "Yongqiang Fan"

    def getPasswordInput(self):
        return "123456"