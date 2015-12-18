# usr/bin/env_python
# coding=utf-8
import socket
import sys
import os
import pickle
import glob
import signal
from socket import *

buf_size=1024
def signal_handler(signal, frame):
    print(' pressed...exiting now')
    sys.exit(0)


def createSocket(PORT):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('',PORT))
    s.listen(5)
    print('Socket criado!\n')
    return s


def criar_socket_c2s(PORT):
    """ criação do socket TCP """
    serverName = '127.0.0.1' # ou nome/ip da maquina onde o servidor se encontra a correr
    clientSocket = socket(AF_INET, SOCK_STREAM)


    print('Socket Created!')


    return clientSocket

def download(fd, fname, fdD):
    if(fname in glob.glob('*.*')):
        buffer=fd.recv(buf_size).decode('utf-8')
        size=os.stat(fname).st_size
        fd.send((str(size)).encode('utf-8'))
        buffer=fd.recv(buf_size).decode('utf-8')
        with open(fname, 'rb') as f:
            string=f.read(buf_size)
            while(string): #send file
                fd.send(string)
                string=f.read(buf_size)
        buffer=fd.recv(buf_size).decode('utf-8')
        print(buffer)
    else:
        buffer=lig_serv('DOWNLOAD '+fname, fdD) #cliente preparado para enviar
        fdD.send('Pronto a receber'.encode('utf-8'))
        size=fdD.recv(buf_size).decode('utf-8')
        if('Tente novamete' not in size):
            fd.send(size.encode('utf-8')) #envia ao cliente o tamanho do file
            buffer=fd.recv(buf_size).decode('utf-8') # certifica-se que o cliente recebeu o tamanho do file
            fdD.send((buffer).encode('utf-8'))
            buffer=fd.recv(buf_size).decode('utf-8')
            size=int(size)
            while(size>=0): #add file
                string=fdD.recv(buf_size)
                fd.send(string)
                size-=1024
            fdD.send(('Ficheiro adicionado').encode('utf-8'))
            buffer=fd.recv(buf_size).decode('utf-8')
            print(buffer)
        else:
            fd.send(size.encode('utf-8')) #avisa o cliente de que o ficheiro não existe




def listar(fd, fdD):
    buffer=lig_serv('LIST',fdD)
    fd.send((buffer).encode('utf-8'))


def menu(fd, fdD):
    comando=fd.recv(buf_size).decode('utf-8')
    if(' ' in comando):
        comando=comando.split()
    if(comando=='LIST'):
        print('listar:\n')
        listar(fd, fdD)
    elif(comando[0]=='UPLOAD'):
        fd.send(('Opcao recebida').encode('utf-8'))# upload,  cache tem de enviar um sinal ao cliente a dizer que pode receber o file
        print('upload:\n')
        upload(fd,comando[1],fdD)
    else:
        fd.send(('Preparado para enviar').encode('utf-8'))
        print('download:\n')
        download(fd,comando[1], fdD)
    print('Exiting menu')



def cache(fd,fdD):
    if not os.path.exists("/home/daniel/Área de Trabalho/irc/server/convidado"):
        os.chdir("..")
        os.makedirs("server/convidado")
    menu(fd,fdD)

def lig_serv(buffer,fdD):
    fdD.connect(('127.0.0.1',9100))
    fdD.send(('3').encode('utf-8'))#inicia sessao covidado no servidor
    buf=fdD.recv(buf_size).decode('utf-8') #recebe inf a dizer que o convidado entrou no servidor
    fdD.send(buffer.encode('utf-8'))
    buffer=fdD.recv(buf_size).decode('utf-8')
    return buffer #devolve uma string que foi enviada pelo servidor para a cache


def upload(fd,fname,fdD):
    size=fd.recv(buf_size).decode('utf-8')
    if(fname in glob.glob('*.*')):
        print('já existe')
        fd.send(('Ficheiro ja existente. Tente novamente').encode('utf-8'))
    else:
        buffer=lig_serv('UPLOAD '+fname, fdD)
        print(buffer)
        if(buffer=='Pronto a receber'):
            fdD.send((size).encode('utf-8'))
            buffer=fdD.recv(buf_size).decode('utf-8')
            print(buffer)
            size=int(size)
            fd.send(('Size received').encode('utf-8'))
            with open(fname, 'wb') as f:
                while(size>=0): #add file
                    buffer=fd.recv(buf_size)
                    f.write(buffer)
                    fdD.send(buffer)
                    size-=1024

            fd.send(('Ficheiro adicionado').encode('utf-8'))
            fdD.close()
        else:
            fd.send((buffer).encode('utf-8'))


def main():
        fd_c=createSocket(9000)#criar a socket
        while 1:
            client, addr = fd_c.accept()
            fdD=criar_socket_c2s(9100)
            pid = os.fork()
            if pid==0:
                buffer=client.recv(buf_size).decode('utf-8')
                client.send(('Login como convidado').encode('utf-8'))
                cache(client,fdD)
                #aux = fd.recv(buf_size).decode('utf-8')
                client.close()
                sys.exit(0)




main()