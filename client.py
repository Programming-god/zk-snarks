import socket 
from phe import paillier 
import json

def serialization():
    global serialised, public_key, private_key
    public_key, private_key = paillier.generate_paillier_keypair()
    secret_num = 3
    secret_num2 = 2
    secret_num3 = 5
    encrypt1 = public_key.encrypt(secret_num)
    encrypt2 = public_key.encrypt(secret_num2)
    encrypt3 = public_key.encrypt(secret_num3)
    encrypted_nums = [encrypt1, encrypt2, encrypt3]
    enc_public_key = {}
    enc_public_key ['public_key'] = {'g': public_key.g, 'n' :public_key.n} #storing a value of a g into g and a value of n into n, and into public key 
    enc_public_key ['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_nums]
    serialised = json.dumps(enc_public_key)#stores public key and values and encryption into variable serialised

def product(data):
    rec_dict2 = json.loads(data) 
    enc_num_rec2 = [paillier.EncryptedNumber(public_key, int(x[0]), int(x[1])) for x in rec_dict2['values']] #deseralise values
    m = private_key.decrypt(enc_num_rec2[0])#acess first element in 0     for example x is list and [0] calls first in list
    print("Answer is:", m)

host = socket.gethostname()  # if same pc
port = 5000  # socket server port number
client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server
serialization()
client_socket.send(serialised.encode())  # send message
data = client_socket.recv(1000000).decode()  # receive response
print('Received from server: ' + data)  # show in terminal
product(data)
client_socket.close()  # close the connection