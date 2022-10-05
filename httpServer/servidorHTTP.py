import socket

host = "127.0.0.1"
porta = 8080

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

infos_do_servidor = (host,porta)

servidor.bind(infos_do_servidor)
servidor.listen(1)

while True:
    conexao, cliente = servidor.accept()

    requisicao = conexao.recv(2048).decode()
    req = requisicao.splitlines()
    print(requisicao)

    if req[0] == "GET / HTTP/1.1":
        f = open("index.html", "r")
        content = f.read()
        f.close()
        response = 'HTTP/1.0 200 OK\n\n' + content
    elif req[-1] == "text=admin&password=admin" and req[0] == "POST / HTTP/1.1":
        f = open("sucesso.html", "r")
        content = f.read()
        f.close()
        response = 'HTTP/1.0 200 OK\n\n' + content

    elif req[-1] != "text=admin&password=admin" and req[0] == "POST / HTTP/1.1":
        f = open("sucessoReverso.html", "r")
        content = f.read()
        f.close()
        response = 'HTTP/1.0 401 Unauthorized\n\n' + content
    else:
        response = 'HTTP/1.0 200 OK\n\n' + '<h1>Erro</h1>'

    conexao.sendall(response.encode())
    conexao.close()
