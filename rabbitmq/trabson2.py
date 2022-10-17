### Aluno: Vinicius Ribeiro de Lima
### Trabalho de sistemas distribuidos




### Imports

import PySimpleGUI as sg
import pika
from threading import Thread
import sys



### Algumas variaveis

border_size = 2 # tamanho das bordas
tamanho = 60 # tamanho de inputs
sg.theme("DarkBlue4") # corzinha
#sg.theme("DarkPurple1")

global mensagensThread # guardar mensagens da thread receptor para pegar essas mensagens e mostrar na tela
mensagensThread = [] 
mensagens = "" # variavel para mostrar na tela as mensagens, do tipo string
global mensagensThread2 # guardar mensagens da thread receptorGrupo para pegar essas mensagens e mostrar na tela
mensagensThread2 = [] 
mensagens2 = "" # variavel para mostrar na tela as mensagens do grupo, do tipo string

global i
i = 0 # variavel int para ajudar a mostrar as mensagens na tela de forma organizada (limitar o numero de mensagens que aparece por vez)
global j
j = 0 # mesmo proposito que a variavel i, porem para a tela grupos

global pararThread # variavel global para quando o programa for fechado, fechar tambem a thread receptor 
pararThread = True

global pararThread2 # variavel global para quando o programa for fechado, fechar tambem a thread receptorGrupos
pararThread2 = True

global usuario # guardar o usuario e passar para thread receptor e para funcao de mandar msg
usuario = ''

global grupo
grupo = ''

#########################################################################
##### Definindo os layouts das duas telas (login e aplicacao em si) #####
#########################################################################

# Layout tela "Login"
login = [
    [sg.Text("Digite seu usuario")],
    [sg.InputText(do_not_clear=False, key='user'), sg.OK("Iniciar")],
]

# Layout tela "Enviar"
Enviar = [  
            [sg.Text('Destinatario:')],
            [sg.InputText(do_not_clear=False, key='Destinatario', size=tamanho)],
            [sg.Text('Digite uma mensagem:')],
            [sg.InputText(do_not_clear=False, key="Mensagem", size=tamanho)],
            [sg.Text('')],
            [sg.OK("Enviar", size=tamanho)],
            
        ]

# Layout tela "Recebidos"
Recebidos = [  
            [sg.Text('Suas mensagens:')],
            #[sg.Button("Atualizar")],
            #[sg.Combo(mensagens, key="msgs", size=15)],
            #[sg.Column(msgs, scrollable=True, vertical_scroll_only=True, size=350, key="coluna")],
            [sg.Text(mensagens, key="msgs")]
            
        ]

# Layout tela "Grupos"
Grupos = [  
            [sg.Text('')],
            [sg.Text('Digite o nome do grupo:')],
            [sg.Text('')],
            [sg.InputText(do_not_clear=False, key="Grupo", size=tamanho)],
            [sg.Text('')],
            [sg.OK("Entrar", size=tamanho)],
        ]

# Layout tela "Configuracoes"
Configuracoes = [
        [sg.Text('')],
        [sg.Text('', key="configUser")],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Cancel("Fechar", size=tamanho)],
]

# Colocando as telas(layouts) em um "TabGroup" para ser possivel alterar entre as telas
telasPrincipais = [
            [
                sg.TabGroup
                (
                    [
                                [
                                    sg.Tab('Enviar', Enviar, title_color = 'White', border_width = border_size, element_justification = 'left'),
                                    sg.Tab('Recebidos', Recebidos, title_color = 'White', border_width = border_size, element_justification = 'center'),
                                    sg.Tab('Grupos', Grupos, title_color = 'White', border_width = border_size, element_justification = 'left'),
                                    sg.Tab('Configurações', Configuracoes, title_color = 'White', border_width = border_size, element_justification = 'center')
                                ]
                    ],      
                            #tab_location='centertop',
                            #title_color='White', tab_background_color='Gray',selected_title_color='White',
                            #selected_background_color='Gray',
                            border_width = border_size
                ), 
                
                
                
            ]
          ]  

# Layout da tela de um grupo aberto

def telaGrupos():
    sg.theme("DarkBlue4")
    #sg.theme("DarkPurple1")
    openGrupo = [ 
            [sg.Text("", key='GrupoTal')],# sg.Button("Update")],
            [sg.Text(mensagens2, key="msgs2")],
            [sg.InputText(do_not_clear=False, key="MensagemGrupo", size=tamanho), sg.Button("Send")],
            [sg.Button("Voltar")],
    ]
    return sg.Window("Grupos", openGrupo, finalize=True)

### -> Tela de login para pegar o nome de quem vai estar usando a aplicaçao e criar uma fila para ela
### -> Loop para eventos da tela de login

telaLogin = sg.Window("Bem vindo", login)

while True:

    event,values = telaLogin.read()

    if event in (sg.WIN_CLOSED, 'Fechar'):
        break
    
    # Quando o botão "Iniciar" for clicado vai ser pego o usuario do campo de input e feita todas as configurações para o rabbitmq
    if event == "Iniciar":
        if values['user'] != '':
            usuario = values['user']

            credentials = pika.PlainCredentials('admin', 'ads2020') 

            connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost',
                                            5672,
                                            '/',
                                            credentials)) 


            channel = connection.channel()

            channel.queue_declare(queue=usuario)

            telaLogin.close()
            break
        if values['user'] == '':
            sg.popup("Você não digitou o usuario!", title=":(")





#### Aplicação em si --->

## Criando a tela da aplicacao
global app
app = sg.Window("Whatsapp 2", telasPrincipais, finalize=True)
appGrupos = None

# funcao receptor para receber as mensagens da sua respectiva fila
def receptor():
    credentials = pika.PlainCredentials('admin', 'ads2020')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost',
                                        5672,
                                        '/',
                                        credentials))

    channel = connection.channel()

    channel.queue_declare(queue=usuario)
    
    def callback(ch, method, properties, body):
        #i = 0
        global i
        global mensagens
        #mensagens = ""
        #print(" [x] Mensagem recebida %r" % body.decode('utf-8'))
        mensagensThread.append(body.decode('utf-8'))
        #print(pararThread)
        if len(mensagensThread) > 0:
            if i == 4:
                i = 1
                mensagens = "\n" + str(mensagensThread[0])
                mensagensThread.pop(0)
                app['msgs'].update(mensagens)
            else:
                i+=1
                mensagens = mensagens + "\n" + str(mensagensThread[0])
                mensagensThread.pop(0)
                app['msgs'].update(mensagens)
        if pararThread == False:
            sys.exit()
            
    channel.basic_consume(queue=usuario, on_message_callback=callback, auto_ack=True)

    #print(' [*] Aguardando mensagens')
    channel.start_consuming()

thread = Thread(target=receptor)
thread.start()

# funcao receptorGrupo para receber as mensagens do grupo
def receptorGrupo():
    #print("Receptor Grupo")
    credentials = pika.PlainCredentials('admin', 'ads2020')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost',
                                        5672,
                                        '/',
                                        credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange=grupo, exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)

    queue_name = result.method.queue

    channel.queue_bind(exchange=grupo, queue=queue_name)
    
    #print(' [*] Aguardando mensagem. Para sair pressione CTRL+C')

    def callback(ch, method, properties, body):
        #print(" [x] %r" % body)
        global j
        global mensagens2
        mensagensThread2.append(body.decode('utf-8'))
        if len(mensagensThread2) > 0:
            if j == 10:
                j = 1
                mensagens2 = "\n" + str(mensagensThread2[0])
                mensagensThread2.pop(0)
                appGrupos['msgs2'].update(mensagens2)
            else:
                j+=1
                mensagens2 = mensagens2 + "\n" + str(mensagensThread2[0])
                mensagensThread2.pop(0)
                appGrupos['msgs2'].update(mensagens2)
        if pararThread2 == False:
            sys.exit()
        #print(pararThread2)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

app['configUser'].update('Usuario = ' + usuario)

while True:

    window,event,values = sg.read_all_windows() #app.read()

    
    if window == app and event in (sg.WIN_CLOSED, 'Fechar'):
        pararThread = False
        channel.basic_publish(exchange='', routing_key=usuario, body="".encode('utf-8'))
        connection.close()
        break

    # Eventos da tela "Enviar"
    if event == "Enviar":
        if values['Mensagem'] != '':
            mensagem = f"{usuario}: {values['Mensagem']}"
            mensagem = mensagem.encode('utf-8')
            destinatario = values['Destinatario'].encode('utf-8')
            channel.basic_publish(exchange='', routing_key=destinatario, body=mensagem)
        if values['Mensagem'] == '':
            sg.popup("Você não digitou nenhuma mensagem!", title=":(")

    # Eventos da tela "Recebidos"
    #if event == "Atualizar":
        #print(len(mensagensThread))
        #if len(mensagensThread) > 0:
          #  if i == 4:
           #     i = 1
            #    mensagens = "\n" + str(mensagensThread[0])
             #   mensagensThread.pop(0)
              #  app['msgs'].update(mensagens)
            #else:
             #   i+=1
              #  mensagens = mensagens + "\n" + str(mensagensThread[0])
               # mensagensThread.pop(0)
                #app['msgs'].update(mensagens)
      

    # Eventos da tela "Grupos"

    if window == appGrupos and event == sg.WIN_CLOSED:
        pararThread = False
        channel.basic_publish(exchange='', routing_key=usuario, body="".encode('utf-8'))
        pararThread2 = False
        channel.basic_publish(exchange=grupo, routing_key='', body=''.encode('utf-8'))
        connection.close()
        break

    if window == app and event == "Entrar":
        appGrupos = telaGrupos() #sg.Window("Grupsdadado", openGrupo, finalize=True)
        grupo = values["Grupo"]
        appGrupos['GrupoTal'].update(f'Grupo {grupo}')
        app.hide()
        channel.exchange_declare(exchange=grupo, exchange_type='fanout')
        thread2 = Thread(target=receptorGrupo)
        thread2.start()
        pararThread2 = True

    if window == appGrupos and event == "Voltar":
        appGrupos.close()
        app.un_hide()
        pararThread2 = False
        channel.basic_publish(exchange=grupo, routing_key='', body='')
        mensagensThread2 = [] 
        mensagens2 = ''
        
        

    if window == appGrupos and event == "Send":
        if values['MensagemGrupo'] != '':
            mensagem = f"{usuario}: {values['MensagemGrupo']}"
            mensagem = mensagem.encode('utf-8')
            channel.basic_publish(exchange=grupo, routing_key='', body=mensagem)
        if values['MensagemGrupo'] == '':
            sg.popup("Você não digitou nenhuma mensagem!", title=":(")


    if window == appGrupos and event == "Update":
        if len(mensagensThread2) > 0:
            if j == 10:
                j = 1
                mensagens2 = "\n" + str(mensagensThread2[0])
                mensagensThread2.pop(0)
                appGrupos['msgs2'].update(mensagens2)
            else:
                j+=1
                mensagens2 = mensagens2 + "\n" + str(mensagensThread2[0])
                mensagensThread2.pop(0)
                appGrupos['msgs2'].update(mensagens2)

app.close()  
