import playground
from playground.network.common import StackingTransport, StackingProtocolFactory, StackingProtocol

class PassThrough1(StackingProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        print("pass through 1 connection made")
        higherTransport = StackingTransport(transport)
        self.higherProtocol().connection_made(higherTransport)

    def data_received(self, data):
        print("pass through 1 data received")
        self.higherProtocol().data_received(data)

    def connection_lost(self, exc):
        print("pass through 1 connection lost")
        self.higherProtocol().connection_lost(exc)


class PassThrough2(StackingProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        print("pass through 2 connection made")
        higherTransport = StackingTransport(transport)
        self.higherProtocol().connection_made(higherTransport)

    def data_received(self, data):
        print("pass through 2 data received")
        self.higherProtocol().data_received(data)

    def connection_lost(self, exc):
        print("pass through 2 connection lost")
        self.higherProtocol().connection_lost(exc)