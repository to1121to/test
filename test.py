import socket
import os
import hashlib
 
server = socket.socket()
server.bind(("192.168.1.17", 12346)) 
server.listen(5) 
print("Waiting for connection...")
while True:
    conn, addr = server.accept() 
print("conn:", conn, "\naddr:", addr) 
while True:
    data =conn.recv(1024) 
    if not data: 
        print("Client has disconnected")   
        break
print("Receive command:", data.decode("utf-8"))
cmd, filename = data.decode("utf-8").split(" ")
if cmd=="get":
    if os.path.isfile(filename):    
size = os.stat(filename).st_size 
conn.send(str(size).encode("utf-8"))    
print("Sent size: ", size)       
conn.recv(1024) 
m = hashlib.md5()   
f = open(filename, "rbname") 
for line in f:
    conn.send(line)  
    m.update(line)
f.close()     
md5 = m.hexdigest()   
conn.send(md5.encode("utf-8"))    
print("md5: ", md5)
server.close()