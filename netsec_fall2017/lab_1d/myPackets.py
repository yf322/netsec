from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import BOOL, STRING


class LogInWithUsername(PacketType):
    DEFINITION_IDENTIFIER = "lab1d.yongqiang.LogInWithUsername"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("username", STRING),
        ("password", STRING)
    ]


class LogInStatus(PacketType):
    DEFINITION_IDENTIFIER = "lab1d.yongqiang.LogInStatus"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("status", BOOL),
        ("userID", STRING)
    ]


class GetUserProfleWithID(PacketType):
    DEFINITION_IDENTIFIER = "lab1d.yongqiang.GetUserProfleWithID"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("userID", STRING)
    ]

class SendUserProfile(PacketType):
    DEFINITION_IDENTIFIER = "lab1d.yongqiang.SendUserProfile"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("profile", STRING)
    ]
