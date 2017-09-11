from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import BOOL, STRING

class LogInStatus(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.yongqiang.LogInStatus"
    DEFINITION_VERSION = "1.0"	
    
    FIELDS = [
        ("status", BOOL), 
        ("userID", STRING)
    ]


