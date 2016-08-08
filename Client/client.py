import socket, asyncore

class ClientUDP(asyncore.dispatcher):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer = ""
        self.data = []

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind(('', 0))

        print "Connecting..."

    def handle_connect(self):
        print "Connected"

    def handle_close(self):
        self.close()

    def handle_read(self):
        data, addr = self.recvfrom(8192)
        self.data += data.split('|')

    def handle_write(self):
        if self.buffer != "":
            sent = self.sendto(self.buffer, (self.host, self.port))
            self.buffer = self.buffer[sent:]
			
    def buildPacket(self, command, value):
        if self.buffer != "":
            self.buffer += '|'
            self.buffer += str(command)
            self.buffer += "*"
            self.buffer += str(value)
        else:
            self.buffer += str(command)
            self.buffer += "*"
            self.buffer += str(value)
        
    def getData(self):
        if self.data:
            return self.data.pop(0)
        return ""