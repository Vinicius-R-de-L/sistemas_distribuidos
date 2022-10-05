import socket
import threading
#import time


# Host e porta para usar na funcao de servidor, variavel infos_do_servidor (tupla) para passar no bind
host = "127.0.0.10"
porta = 2130
infos_do_servidor = (host,porta)

# Hosts e portas que esse nó vai conhecer e mandar as mensagens
hosts = ["127.0.0.11", "127.0.0.13"]
portas = [2131, 2133]

# Criação do socket para função cliente e servidor
#socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectando aos outros hosts
""" infos_dos_outros_nodes = (hosts[0],portas[0])
socket_cliente.connect(infos_dos_outros_nodes) """

socket_servidor.bind(infos_do_servidor)
socket_servidor.listen()

global mensagens
mensagens = []
global anterior
anterior = '' 



def Cliente():
    while True:

        #for i in mensagens:
            #try:
                #onteudoMensagem.append(i.split('#-')[0]) 
                #visualizadoresMensagem.append(i.split('#-')[1])

                #visualizadoresMensagem = visualizadoresMensagem[0].split()
            #except:
               # pass

        print("\nEscolha uma opção abaixo: ")
        print("1) Enviar mensagem")
        print("2) Ver mensagens")
        print("3) Apagar mensagens")
        opcao = int(input())

        if opcao == 1:
            socket_cliente = []
            for i in range(len(hosts)):
                socket_cliente.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

            for i in range(len(hosts)):
                infos_dos_outros_nodes = (hosts[i],portas[i])
                try:
                    socket_cliente[i].connect(infos_dos_outros_nodes)
                except:
                    pass
            
            #mensagem = "Mensagem: "
            #mensagem += input("Digite a sua fofoca: ")
            #mensagem += f' Recebida de: {host} '
            mensagem = input('\nDigite a sua fofoca: ')
            mensagem = mensagem.encode()
            
            global mensagens
            mensagens.append(mensagem.decode())

            for i in range(len(hosts)):
                try:
                    socket_cliente[i].send(mensagem)
                except:
                    pass    
                #print(socket_cliente[i])

            for i in range(len(hosts)):
                socket_cliente[i].close()

        if opcao == 2:
            mensagens = list(dict.fromkeys(mensagens))
            print("\nLista de mensagens: \n")
            for msg in mensagens:
                    print(msg)
        
        if opcao == 3:
            mensagens = [] 

def Servidor():
    anterior = ''
    while True:
        conexao, cliente = socket_servidor.accept()
        mensagem = conexao.recv(2048).decode()

        if anterior != mensagem:
            for msg in mensagens:
                if msg == mensagem:
                    pass
                if msg != mensagem:
                    socket_cliente = []

                    for i in range(len(hosts)):
                        socket_cliente.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

                    for i in range(len(hosts)):
                        infos_dos_outros_nodes = (hosts[i],portas[i])
                        try:
                            socket_cliente[i].connect(infos_dos_outros_nodes)
                        except:
                            pass

                    for i in range(len(hosts)):
                        try:
                            socket_cliente[i].send(mensagem.encode())
                        except:
                            pass   

                    for i in range(len(hosts)):
                        socket_cliente[i].close()
        
        anterior = mensagem
        mensagens.append(mensagem)

threading.Thread(target=Cliente).start()
threading.Thread(target=Servidor).start()
#close = False
