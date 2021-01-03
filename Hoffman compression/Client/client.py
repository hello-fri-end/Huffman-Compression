import os
import socket
import pickle
from huffman2 import HuffmanCoding

PORT= 9001
IP=''
conn=(IP,PORT)

if __name__== "__main__":
    client_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(conn)

    input_file=  os.path.join(os.getcwd(),"testfile.txt")

    #compress the text file with huffman encdoing
    H= HuffmanCoding(input_file)
    output_file= H.compress()

    #send reverse mapping
    reverse_mapping= H.reverse_mapping
    serialized_reverse_mapping= pickle.dumps(reverse_mapping)
    client_socket.send(serialized_reverse_mapping)
    with open(output_file,'rb') as output:
        data= output.read(1024)
        client_socket.send(data)
        print("Sent Successfully")


    client_socket.close()

    
