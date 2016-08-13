import socket, asyncore

class ServerUDP(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.clientA = None
        self.clientB = None
        self.bufferA = ""
        self.bufferB = ""
        self.data = []

    def handle_connect(self):
        print "Server started..."

    def handle_read(self):
        buff, addr = self.recvfrom(8192)
		
        #check if server connected to two clients already
        if self.clientA == None:
            self.clientA = addr
        elif self.clientB == None and addr != self.clientA:
            self.clientB = addr

        #if data received from clientA or clientB, process packet
        if self.clientA == addr or self.clientB == addr:
            packets = buff.split('|')
            for p in packets:
                p = str(addr) + '*' + str(p)
                self.data.append(p)
		
	
    def handle_write(self):
        if self.bufferA != "":
            if self.clientA != None:
                sentA = self.sendto(self.bufferA, self.clientA)
                self.bufferA = self.bufferA[sentA:]
        if self.bufferB != "":
            if self.clientB != None:
                sentB = self.sendto(self.bufferB, self.clientB)
                self.bufferB = self.bufferB[sentB:]
                
		
	#update packets for A and B
    def buildPacket(self, command, value):
        self.buildAPacket(command, value)
        self.buildBPacket(command, value)

    def buildAPacket(self, command, value):
        if self.bufferA != "":
            self.bufferA += '|'
            self.bufferA += str(command)
            self.bufferA += "*"
            self.bufferA += str(value)
        else:
            self.bufferA += str(command)
            self.bufferA += "*"
            self.bufferA += str(value)

    def buildBPacket(self, command, value):
        if self.bufferB != "":
            self.bufferB += '|'
            self.bufferB += str(command)
            self.bufferB += "*"
            self.bufferB += str(value)
        else:
            self.bufferB += str(command)
            self.bufferB += "*"
            self.bufferB += str(value)

            
    #return next element in data array and remove it from the array
    def getData(self):
        if self.data:
            return self.data.pop(0)
        return ""