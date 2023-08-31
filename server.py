import socket
from phe import paillier 
import json 


def finalCalculation(data):
    global serialised2
    rec_dict = json.loads(data) #set equal to file 
    pk = rec_dict['public_key'] #return public key to numbers 
    public_key_rec = paillier.PaillierPublicKey(n=int(pk['n'])) #assign integer to deserialise values of n and g 
    enc_nums_rec = [paillier.EncryptedNumber(public_key_rec, int(x[0]), int(x[1])) for x in rec_dict['values']] #deseralise values
    a = 3
    a2 = 5
    a3 = 6
    b = 0
    y = a*enc_nums_rec[0] + a2 *enc_nums_rec[1] + a3*enc_nums_rec[2] +b
    r = [y] 
    enc_public_key2 = {}
    enc_public_key2['public_key'] = {'g': public_key_rec.g, 'n' :public_key_rec.n} #storing a value of a g into g and a value of n into n, and into public key 
    enc_public_key2 ['values'] = [(str(x.ciphertext()), x.exponent) for x in r]
    serialised2 = json.dumps(enc_public_key2)   

host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number(must be above 2400)

server_socket = socket.socket()  # instantiate, declare 
server_socket.bind((host, port))  # connect to the client
server_socket.listen(2)
conn, address = server_socket.accept()
print("Connection from" + str(address))
data = conn.recv(1000000).decode()
print('From user: ' + data)
finalCalculation(data)  # show in terminal
conn.send(serialised2.encode())
conn.close()  # close the connection
