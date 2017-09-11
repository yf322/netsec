from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER


class GetUserProfleWithID(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.yongqiang.GetUserProfleWithID"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("userID", STRING)
    ]
