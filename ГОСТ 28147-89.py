import operator
import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

text=input('Введите открытый текст: ')
key=randomword(32)
key=[key[i:i+4] for i in range(0, len(key), 4)]


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)

#table substitutions
podstanovki=[[1,13,4,6,7,5,14,4],[15,11,11,12,13,8,11,10],[13,4,10,7,10,1,4,9],[0,1,0,1,1,13,12,2],[5,3,7,5,0,10,6,13],[7,15,2,15,8,3,13,8],[10,5,1,13,9,4,15,0],[4,9,13,8,15,2,10,14],[9,0,3,4,14,14,2,6],[2,10,6,10,4,15,3,11],[3,14,8,9,6,12,8,1],[14,7,5,14,12,7,1,12],[6,6,9,0,11,6,0,7],[11,8,12,3,2,0,7,15],[8,2,15,11,5,9,5,5],[12,12,14,2,3,11,9,3]]

def rayndR(X,L,R):
    F_RX = (int(R, 2) + int(X, 2)) % (2 ** 32)
    table = [int(''.join(i), 2) for i in grouper(bin(F_RX)[2:], 4)]
    new_table = []
    binary_vid = ''
    for i in range(len(table)):
        new_table.append(podstanovki[table[i]][i])
        binary_vid = binary_vid + ('0' * (4 - len(bin(podstanovki[table[i]][i])[2:]))) + bin(podstanovki[table[i]][i])[2:]
    sdvig = binary_vid[11:] + binary_vid[:11]
    R_1 = bin(operator.xor(int(sdvig, 2), int(L, 2)))[2:]
    R_1 = ('0' * (32 - len(R_1))) + R_1
    res=[]
    res.append(R)
    res.append(R_1)
    return res



def encryption(podstanovki,text,key):
    binary_text = [bin(i)[2:] for i in list(text.encode('cp1251'))]
    binary_text = ['0' * (8 - len(i)) + i for i in binary_text]
    L = ''.join(binary_text[:4])
    R = ''.join(binary_text[4:])
    for round in range(24):
        binary_key = [bin(i)[2:] for i in list(key[round%8].encode('cp1251'))]
        X = ''.join(['0' * (8 - len(i)) + i for i in binary_key])
        res=rayndR(X,L,R)
        R=res[1]
        L=res[0]
    for round in range(8):
        binary_key = [bin(i)[2:] for i in list(key[-round-1].encode('cp1251'))]
        X = ''.join(['0' * (8 - len(i)) + i for i in binary_key])
        res = rayndR(X, L, R)
        R = res[1]
        L = res[0]
    return R+L

def decryption(podstanovki,text,key):
    binary_text = [bin(i)[2:] for i in list(text.encode('cp1251'))]
    binary_text = ['0' * (8 - len(i)) + i for i in binary_text]
    L = ''.join(binary_text[:4])
    R = ''.join(binary_text[4:])
    for round in range(8):
        binary_key = [bin(i)[2:] for i in list(key[round].encode('cp1251'))]
        X = ''.join(['0' * (8 - len(i)) + i for i in binary_key])
        res = rayndR(X, L, R)
        R = res[1]
        L = res[0]
    for round in range(24):
        binary_key = [bin(i)[2:] for i in list(key[(-round-1)%(-8)].encode('cp1251'))]
        X = ''.join(['0' * (8 - len(i)) + i for i in binary_key])
        res = rayndR(X, L, R)
        R = res[1]
        L = res[0]
    return R+L


message=[text[i:i+8] for i in range(0, len(text), 8)]
konez=''
konez1=''
for i in range(len(message)):
    text=message[i]
    result=encryption(podstanovki,text,key)
    result=[result[i:i+8] for i in range(0, len(result), 8)]
    otvet=bytearray([(int(j,2)) for j in result]).decode('cp1251')
    konez1 += otvet
    print(otvet)
    binary_text = [bin(i)[2:] for i in list(otvet.encode('cp1251'))]


    result1=decryption(podstanovki,otvet,key)
    result1=[result1[i:i+8] for i in range(0, len(result1), 8)]
    otvet1=bytearray([(int(j,2)) for j in result1]).decode('cp1251')
    print(otvet1)
    konez+=otvet1
if len(message)>1:
    print(konez1)
    print(konez)