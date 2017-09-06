from playground.network.packet import PacketType
from loginUsername import LogInWithUsername
from loginStatus import LogInStatus
from getUserProfile import GetUserProfileWithID
from sendUserProfile import SendUserProfile

packet1 = LogInWithUsername()
packet1.username = "Yongqiang Fan"
packet1.password = b"There are a lot of works in lab2b than lab2a."

packetBytes = packet1.__serialize__()

packet2 = PacketType.Deserialize(packetBytes)
if packet1 == packet2:
	print("yes")



