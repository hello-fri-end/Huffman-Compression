import os
import heapq

class HuffmanCoding:
    def __init__(self,path):
        self.path= path
        self.heap=[] #min heap for huffman tree
        self.codes={} #dictionary of charcter as key and code as value
        self.revere_mapping= {} #code to character

    class HeapNode:
        def __init__(self,char,freq):
            self.char= char
            self.freq= freq
            self.left= None
            self.right= None

        def __lt__(self,other):
            return self.freq < other.freq

        def __eq__(self, other):
            if(other==None):
                return -1
            return self.freq== other.freq

    def make_frequency_dict(self,text):
        #return frequncy of occurence of each character
        frequency= {}
        for character in text:
            if not character in frequency:
                frequency[character]=0
            frequency[character]+=1
        return frequency
    
    def make_heap(self,frequency):
        #makes priority queue
        for key in frequency:
            node= self.HeapNode(key,frequency[key])
            #good boy python, heapq will ensure min heap property is followed
            heapq.heappush(self.heap,node)



    def merge_nodes(self):
        while(len(self.heap)>1):
            node1= heapq.heappop(self.heap)
            node2= heapq.heappop(self.heap)
            merged= self.HeapNode(None, node1.freq + node2.freq)
            merged.left= node1
            merged.right= node2

            heapq.heappush(self.heap,merged)

    def make_codes_helper(self,node,current_code):
        if(node == None):
            return
        if(node.char!= None): #implies leaf node
            self.codes[node.char]= current_code
            self.revere_mapping[current_code]= node.char

        #call the function recursively
        self.make_codes_helper(node.left, current_code + "0")
        self.make_codes_helper(node.right, current_code + "1")

    def make_codes(self):
        #assigns codes based on the huffman tree
        root= heapq.heappop(self.heap)
        current_code=""
        self.make_codes_helper(root,current_code)


    def get_encoded_text(self,text):
        #replace characters with code and return
        encoded=""
        for character in text:
            endcoded_text+= self.codes[character]
        return endcoded_text

    def pad_encoded_text(self,endcoded_text):
        #pad endcoded_text and return
        extra_padding= 8 - len(endcoded_text)%8
        for i in range(extra_padding):
            endcoded_text +="0"

        padded_info= "{0:08b}".format(endcoded_text)
        encoded_text= padded_info + endcoded_text
        return encoded_text

    def get_byte_array(self,padded_encoded_text):
        #convrt bits into bytes.Return byte array.
        b= bytearray()
        for i in range(0,len(padded_encoded_text)):
            byte= padded_encoded_text[i:i+8]
            b.append(int(byte,2) )
        return b

    def compress(self):
        filename,file_extension= os.path.splitext(self.path)
        output_path= filename + ".bin"

        with open(self.path, 'r') as file , open(output_path,'wb') as output:
            text= file.read()
            text= text.rstrip()
        
            #frequency of occurence of each character
            frequency=self.make_frequency_dict(text)
            #build min heap from the frequency dictionary
            self.make_heap(frequency)
            #build huffman tree
            self.merge_nodes()
            #fill the dictionary of codes
            self.make_codes()

        encoded_text= get_encoded_text(text)
        padded_encoded_text= pad_encoded_text(endcoded_text)

        b= self.get_byte_array(padded_encoded_text)
        output.write(bytes(b))

        print("Compressed")
        return output_path

    def remove_padding(self,bit_string):
        #remove padding and return
        paded_info= bit_string[:8]
        extra_padding= int(padded_info,2)
        #remove both padding info and padded zeros
        bit_string= bit_string[8:]
        endcoded_text= bit_string[:-1*extra_padding]

        return  endcoded_text

    def decode_text(self,endcoded_text):
        current_code=""
        decoded_text= ""

        for bit in endcoded_text:
            current_code+= bit
            if(current_code in self.revere_mapping):
                character= self.revere_mapping[current_code]
                decoded_text+=character
                current_code=""
        return decoded_text

    def decompress(self,input_path):
        filename,file_extension= os.path.splitext(input_path)
        output_path= filename + "_decompressed" + ".txt"

        with open(input_path,'rb') as file, open(output_path,'w') as output:
            bit_string= ""
            byte=file.read(1)
            while(len(byte)>0):
                byte= ord(byte)
                bits= bin(byte)[2:].rjust(8,'0') #trim out 0b, pad zeros to make 8 bytes
                bit_sring += bits
                byte=file.read(1)

            endcoded_text= self.remove_padding(bit_string)
            decoded_text= self.decode_text(encoded_text)

            output.write(decode_text)

        print("Decompression complete")
        return output_path







