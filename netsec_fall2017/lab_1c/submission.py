from myPackets import *
from client import ClientProtocol
from server import ServerProtocol
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
import asyncio

def basicUnitTest():
    loop = asyncio.set_event_loop(TestLoopEx())
    client = ClientProtocol(loop)
    server = ServerProtocol()
    transportToServer = MockTransportToProtocol(myProtocol=client)
    transportToClient = MockTransportToProtocol(myProtocol=server)
    transportToServer.setRemoteTransport(transportToClient)
    transportToClient.setRemoteTransport(transportToServer)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)

    loginWithUsername = LogInWithUsername()
    getUserProfile = GetUserProfleWithID()
    client.loginStart(loginWithUsername, getUserProfile)

    assert client.state == 1
    assert server.state == 1

if __name__ == "__main__":
    basicUnitTest()


