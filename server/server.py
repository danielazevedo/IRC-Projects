#usr/bin/env_python
#coding=utf-8
import socket
import sys
import os
import pickle
import signal
from socket import *
import glob
from signal import SIGPIPE,SIG_DFL
#signal(SIGPIPE,SIG_DFL)

buf_size=1024


def sigint(signal, frame):
    print(' pressed...exiting now')
    sys.exit(0)

#alterar
def createSocket(PORT):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('',9100))
    s.listen(5)
    print('Socket criado!\n')
    return s



def cria_user(fd, users,user,pwd):

    if(user in users.keys()):
        fd.send(('Utilizador ja existe\n').encode('utf-8'))
    else:
        users[user]=pwd

        with open('users.pkl', 'wb') as file:
            pickle.dump(users,file, pickle.HIGHEST_PROTOCOL)
        os.mkdir(user)
        os.chdir("/home/daniel/Área de Trabalho/irc/server/"+user)
        fd.send(('Utilizador criado com sucesso').encode('utf-8'))

    print(users.keys())
    return users
        

def download(fd, fname):
    fd.send(('Preparado para enviar').encode('utf-8'))
    buffer=fd.recv(buf_size).decode('utf-8') #socket preparado para receber
    if(fname not in glob.glob('*.*')):
        fd.send(('O ficheiro não existe no servidor. Tente novamente').encode('utf-8'))
    else:
        size=os.stat(fname).st_size
        fd.send((str(size)).encode('utf-8'))
        buffer=fd.recv(buf_size).decode('utf-8')
        with open(fname, 'rb') as f:
            string=f.read(buf_size)
            while(string): #send file
                fd.send(string)
                string=f.read(buf_size)
        buffer=fd.recv(buf_size)


def listar(fd, user):
    files=''
    for file in glob.glob('*.*'):
        files+=file+' '
    if(files==''):
        fd.send(('Não existem ficheiros nesta pasta').encode('utf-8'))
    else:
        fd.send((files).encode('utf-8'))

def upload(fd,fname):
    if(fname in glob.glob('*.*')):
        fd.send(('Ficheiro ja existente. Tente novamente').encode('utf-8'))
    else:
        fd.send(('Pronto a receber').encode('utf-8'))
        f_size=fd.recv(buf_size).decode('utf-8')
        f_size=int(f_size)
        fd.send(('Size received').encode('utf-8'))
        with open(fname, 'wb') as f:
            while(int(f_size)>=0): #add file
                f.write(fd.recv(buf_size))
                f_size-=1024
        fd.send(('Ficheiro adicionado').encode('utf-8'))

    
def login(fd, users,username,password):
    print('Login')
    if(username in users.keys() and users[username]==password ):
        fd.send(('Login feito com sucesso').encode('utf-8'))
        print('Utilizador conectado com sucesso:')
        print(username,password)
        menu(fd, username)
    else:
        fd.send(('A combinacao username + password nao e valida').encode('utf-8'))
        fd.recv(buf_size).decode('utf-8')
        login(fd, users,username,password)


def menu(fd, user):
    os.chdir("/home/daniel/Área de Trabalho/irc/server/"+user)
    comando=''
    while(comando!='LOGOUT'):
        comando=''
        comando+=fd.recv(buf_size).decode('utf-8')
        if(' ' in comando):
            comando=comando.split()
        if(comando=='LIST'):
            print('listar:\n')
            listar(fd, user)
        elif(comando[0]=='UPLOAD'):
            print('upload:\n')
            upload(fd,comando[1])
        elif(comando[0]=='DOWNLOAD'):
            print('download:\n')
            download(fd,comando[1])
    print('Exiting menu')


def divide(answer):
    i=0
    j=0
    c=0
    pw=''
    user=''
    op=answer[0]
    i+=2#para passar a opcao e o espaco
    while answer[i]!=' ':
        user+=answer[i]
        i+=1
    i+=1
    while(i<len(answer)):
        pw+=answer[i]
        i+=1

    return op,user,pw



def main():
    signal.signal(signal.SIGINT, sigint)
    fd=createSocket(9100)#criar a socket
    users={}
    if os.path.isfile('users.pkl') and (os.path.getsize('users.pkl') > 0):#se o ficheiro existir tiver alguma coisa
         with open("users.pkl",'rb') as input:
            users=pickle.load(input)
    else:
        print('Ficheiro nao existe ou esta vazio')



    while 1:    
        client, addr = fd.accept()
        pid = os.fork()
        if pid==0:
            aux = client.recv(buf_size).decode('utf-8')

            aux=aux.split()
            op=aux[0]
            if(op=='3'):
                client.send(('Iniciando sessao como convidado').encode('utf-8'))
                menu(client, 'convidado')
            elif(op=='1' or op=='2'):
                user=aux[1]
                pwd=aux[2]
                if(op=='1'):
                    users=cria_user(client,users,user,pwd)
                elif(op=='2'):
                    login(client,users,user,pwd)
            fd.close()
            sys.exit(0)



main()
