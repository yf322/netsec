from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER

class LogInWithUsername(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.yongqiang.LogInWithUsername"
    DEFINITION_VERSION = "1.0"	
    
    FIELDS = [
        ("username", STRING), 
        ("password", STRING)
    ]


