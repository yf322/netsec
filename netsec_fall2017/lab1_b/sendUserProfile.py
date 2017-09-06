from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER


class SendUserProfile(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.yongqiang.SendUserProfile"
    DEFINITION_VERSION = "1.0"

    FILEDS = [
        ("profile", STRING)
    ]
