from myPackets import  *
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
