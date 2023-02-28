import socket
import pickle
HEADERSIZE = 10


class network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096*4).decode()
        except:
            pass
    
    # Credit: Simon vW(StackOverflow) I believe I mostly understand what they did here
    # this is the function you should use, it uses a receive function that has a buffer
    # and ensures that you receive ALL the information that you sent without throwing errors
    def send_data(self, data):
        data_to_send = pickle.dumps(data)
        data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
        try:
            self.client.send(data_size + data_to_send)
            
            package = self.receive_data()
            return package
        except socket.error as e:
            print(e)

    # Credit: Simon vW(StackOverflow) I believe I mostly understand what they did here
    def receive_data(self):
        full_msg = b''
        new_msg = True
        while True:
            msg = self.client.recv(16)
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
                
            full_msg += msg
    
            if len(full_msg)-HEADERSIZE == msglen:
                data = pickle.loads(full_msg[HEADERSIZE:])
                break
    
        return data
    
    def get_p(self):
        return self.p