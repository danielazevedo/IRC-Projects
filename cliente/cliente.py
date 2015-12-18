# usr/bin/env_python
# coding=utf-8
import socket
import sys
import os
import pickle
import glob
import signal
from socket import *

buf_size = 1024

def sigint(signal, frame):
    print(' pressed...exiting now')
    sys.exit(0)


def criar_socket(PORT):
    """ criação do socket TCP """
    serverName = '127.0.0.1' # ou nome/ip da maquina onde o servidor se encontra a correr
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,PORT))

    print('Socket Created!')


    return clientSocket




def download(fd, file):
        buffer=fd.recv(buf_size).decode('utf-8')
        fd.send(('Pronto a receber').encode('utf-8'))
        f_size=fd.recv(buf_size).decode('utf-8')
        if('Tente novamente' not in f_size): #significa que fd.recv()=tamanho do ficheiro
            f_size=int(f_size)
            fd.send(('Size received').encode('utf-8'))
            with open(file, 'wb') as f:
                while(int(f_size)>=0): #add file
                    f.write(fd.recv(buf_size))
                    f_size-=1024
            fd.send(('Ficheiro adicionado').encode('utf-8'))
            print('Ficheiro adicionado')
        else:
            print(f_size+'\n')



def upload(fd, file):
    buffer=fd.recv(buf_size).decode('utf-8')
    size=os.stat(file).st_size
    fd.send((str(size)).encode('utf-8'))
    buffer=fd.recv(buf_size).decode('utf-8')
    if('Tente novamente' not in buffer):
        with open(file, 'rb') as f: #enviamos o file
            string=f.read(buf_size)
            while(string):
                fd.send(string)
                string=f.read(buf_size)
        buffer = fd.recv(buf_size).decode('utf-8')
        print(buffer + '\n')

    else:
        print(buffer)


def menu(fd):
    comando = ''
    while (comando != 'LOGOUT'):
        comando = input('Introduza um comando (LIST, UPLOAD <file>, DOWNLOAD <file>, LOGOUT):\n')
        fd.send(comando.encode('utf-8'))

        if(comando.split()[0]=='UPLOAD' and comando.split()[1] not in glob.glob('*.*')):
                print('O cliente não tem nenhum ficheiro com esse nome')
        elif((comando.split()[0]=='DOWNLOAD' and comando.split()[1] in glob.glob('*.*'))):
             print('O cliente já tem o ficheiro pedido\n')
        else:
            if(comando=='LIST'):
                string=fd.recv(buf_size).decode('utf-8')
                print('\n\nFICHEIROS NO SERVIDOR:')
                print(string)


            elif('UPLOAD' in comando):
                comando=comando.split()
                fn=comando[1]
                upload(fd,fn)


            elif('DOWNLOAD' in comando):
                comando=comando.split()
                fn=comando[1]
                download(fd,fn)




def convidado():
    fd_c=criar_socket(9000)
    fd_c.send(('3').encode('utf-8'))
    buffer=fd_c.recv(buf_size).decode('utf-8')
    print(buffer) #login como convidado
    menu(fd_c)


def main():
    signal.signal(signal.SIGINT, sigint)
    opcao = 0

    while (opcao != 4):
        opcao = eval(input('1.cria utilizador\n2.login\n3.convidado\n4.exit\n'))
        if(opcao==4):
            print('Exiting...')
            break
        else:
            if opcao==2 or opcao==1:
                fd=criar_socket(9100)
                user=input('Indique o username:\n')
                pw=input('Indique a sua palavra-passe:\n')
                fd.send((str(opcao)+' '+user+' '+pw).encode('utf-8'))
            elif(opcao==3):
                convidado()

            string=fd.recv(buf_size).decode('utf-8')
            print(string)

            if (string=='Login feito com sucesso'):
                menu(fd)


main()
