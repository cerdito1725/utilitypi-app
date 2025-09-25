import socket

def socketTemp():

   ClientSocket = socket.socket()
   host = '192.168.0.232'
   port = 65432

   try:
      ClientSocket.connect((host, port))
   except socket.error as e:
      print(str(e))

   Response = ClientSocket.recv(1024)
   a = Response.decode('utf-8')
   b = int(float(a))
   ClientSocket.close()
   return b

#print(socketTemp())
