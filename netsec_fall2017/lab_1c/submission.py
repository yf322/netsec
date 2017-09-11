
from client import ClientProtocol
from server import ServerProtocol
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
import asyncio

def basicUnitTest():
    loop = asyncio.set_event_loop(TestLoopEx())
    client = ClientProtocol()
    server = ServerProtocol()
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)

if __name__ == "__main__":
    basicUnitTest()


