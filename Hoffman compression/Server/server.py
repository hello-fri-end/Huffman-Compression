import socket
import pickle
import os
from huffman2 import HuffmanCoding

PORT= 9001
IP=''
conn= (IP,PORT)

if __name__ == "__main__":
    server_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(conn)
    server_socket.listen(5)
    c,addr= server_socket.accept()

    #recieve reverse mapping first
    serialized_reverse_mapping= c.recv(1024)
    reverse_mapping= pickle.loads(serialized_reverse_mapping)

    

    input_data= c.recv(1024)
    
    with open("testfile.txt", "wb") as input_file:
        input_file.write(input_data)

    path= os.path.join(os.getcwd(), "testfile.txt")

    #decompress input_file
    H= HuffmanCoding(path)
    H.reverse_mapping= reverse_mapping
    output_file= H.decompress(path)

    print("Recieved and decompressed")

    server_socket.close
