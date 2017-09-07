from playground.network.packet import PacketType
from loginUsername import LogInWithUsername
from loginStatus import LogInStatus
from getUserProfile import GetUserProfleWithID
from sendUserProfile import SendUserProfile

def packet1Test():
    packet1 = LogInWithUsername()
    packet1.username = "Yongqiang Fan"
    packet1.password = "password"

    packet1Bytes = packet1.__serialize__()
    packet1a = LogInWithUsername.Deserialize(packet1Bytes)
    assert packet1 == packet1a

def packet2Test():
    packet2 = LogInStatus()
    packet2.status = True
    packet2.userID = "1"

    packet2Bytes = packet2.__serialize__()
    packet2a = LogInStatus.Deserialize(packet2Bytes)
    assert packet2 == packet2a

def packet3Test():
    packet3 = GetUserProfleWithID()
    packet3.userID = "1"

    packet3Bytes = packet3.__serialize__()
    packet3a = GetUserProfleWithID.Deserialize(packet3Bytes)
    assert packet3 == packet3a

def packet4Test():
    packet4 = SendUserProfile()
    packet4.profile = '{"username": "Yongqiang Fan", "userID": "1"}'

    packet4Bytes = packet4.__serialize__()
    packet4a = SendUserProfile.Deserialize(packet4Bytes)
    assert packet4 == packet4a

def basicUnitTest():
    try:
        packet1Test()
        packet2Test()
        packet3Test()
        packet4Test()
    except:
        print("Unexpected error!")






basicUnitTest()





