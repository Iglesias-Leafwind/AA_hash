
import sys
from os import listdir
from os.path import isfile, join
import time
import string

class HashTable:

    def __init__(self, size=555, hash_function=lambda key,size: hash(key) % size):

        self.size = size
        self.data = [None] * self.size
        self.bool = [0] * self.size
        self.hash_function = hash_function
        
    def __getitem__(self, key):

        return self.get(key)

    def __setitem__(self, key, data):

        self.put(key, data)

    def put(self, key, data):

        hash_value = self.hash_function(key,self.size)
        
        self.data[hash_value] = data
        self.bool[hash_value] = 1
        
    def get(self, key):

        hash_value = self.hash_function(key)
        data = self.data[hash_value]
        return data
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

class Reader:

    def __init__(self):
        self.stopwords = None

    def readFile(self,file_path):
        with open(file_path, "r", encoding="utf-8") as readFile:
            stop_words_en = set(stopwords.words('english'))
            stop_words_pt = set(stopwords.words('portuguese'))
            text = readFile.read()
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
            words = set()
            for word in text.split(" "):
                word = ''.join(filter(str.isalnum,word))
                if(word not in stop_words_en and word not in stop_words_pt):
                    words.add(word)
            return words

def mult(array):
    returning = 1
    for num in array:
        returning *= num
    return returning

def elevated(array):
    returning = len(array) + 1
    for num in array:
        returning **= num
    return returning
import hashlib
import os
if __name__ == '__main__':

    #analise:
    #testar varias hash functions
    #testar varias hash tables e verificar a media de cada uma para ver se da valores diff
    #testar varios tamanhos

    fileFolder = "./texts"
    filePaths = {f:join(fileFolder, f) for f in listdir(fileFolder) if isfile(join(fileFolder, f))}
    reader = Reader()
    hash_function_md5 = lambda word,size : int(hashlib.md5(word.encode()).hexdigest(),16) % size
    hash_function_sha256 = lambda word,size : int(hashlib.sha256(word.encode()).hexdigest(),16) % size

    with open(os.path.join(os.getcwd(),"results.csv"),"w") as results:
        for name,path in filePaths.items():
            print(name)
            words = reader.readFile(path)
            results.write("name,hash table size,exact distinct,approximated distinct default,approximated distinct md5,approximated distinct sha256\n")
            for table_size in range(1000,300000000,1000):
                print(table_size)
                hash_table_default = HashTable(table_size)
                hash_table_md5 = HashTable(table_size,hash_function_md5)
                hash_table_sha256 = HashTable(table_size,hash_function_sha256)
                for word in words:
                    hash_table_default[word] = word
                    hash_table_md5[word] = word
                    hash_table_sha256[word] = word
                results.write(str(name) + "," + str(table_size)+ "," + str(len(words)) + "," + str(sum(hash_table_default.bool)) + "," + str(sum(hash_table_md5.bool)) + "," + str(sum(hash_table_sha256.bool)) + "\n")
    sys.exit(0)
