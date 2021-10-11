import socket
import json
import pdb
import copy

def dict_to_bytes(the_dict):
    string = json.dumps(the_dict).encode('utf-8')
    return(string)

def bytes_to_dict(string):
    the_dict = json.loads(string.decode('utf-8'))
    return(the_dict)


class server_con():
    def __init__(self,host='',port=30):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))



        
    def server_read(self):
        # pdb.set_trace()
        print("Waiting to read ...")
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        print('Connected by', self.addr)
        return_data = {}
        try:
            in_data = self.conn.recv(1024)
            # pdb.set_trace()
            if in_data: return_data = copy.deepcopy(in_data)
            # if not in_data: break
    
            print("Client Says: "+return_data.decode("utf-8"))
            # self.conn.sendall(b"Server Says:hi")
        except socket.error:
            print("Error Occured.")
        
        
        # self.conn.close()
        return(bytes_to_dict(return_data))
    
    def server_write(self,data,host="151.100.55.63",port=30):
        # pdb.set_trace()
        print('Writing values ...')
        self.conn.sendall(dict_to_bytes(data))

# def server_read(host='',port=30):
#     # host = ''        # Symbolic name meaning all available interfaces
#     # port = 30     # Arbitrary non-privileged port
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((host, port))
    
#     print(host , port)
#     s.listen(1)
#     conn, addr = s.accept()
#     print('Connected by', addr)
#     return_data = {}
#     while True:
    
#         try:
#             in_data = conn.recv(1024)
#             # pdb.set_trace()
#             if in_data: return_data = copy.deepcopy(in_data)
#             if not in_data: break
    
#             print("Client Says: "+return_data.decode("utf-8"))
            
#             conn.sendall(b"Server Says:hi")
    
#         except socket.error:
#             print("Error Occured.")
#             break
    
    
#     conn.close()
#     return(bytes_to_dict(return_data))
#     # return(return_data)