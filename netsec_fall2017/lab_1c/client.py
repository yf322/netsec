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
        self.state = 0

    def connection_made(self, transport):
        print("Connected to the server")
        self.transport = transport

    def data_received(self, data):
        self._deserializer = PacketType.Deserializer()
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
                self.transport = None
                print("Error packet from server")
                sys.exit(1)

    def connection_lost(self, exc):
        self.transport = None
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