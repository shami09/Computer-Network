from logging.handlers import SocketHandler
import socket
import sys
from os.path import exists

def generateSocket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("",port))
    except Exception:
        print(Exception, sys.stderr,)
        sys.exit(-1)
    return sock

def listenToRequests(sock,port):
    sock.listen(1)
    print("Listening for all IP addresses on port " +str(port))
    while True:
        client,client_addr = sock.accept()
        request = client.recv(2048).decode().split("\n")[0].split(" ")[1]
        fileType = request.split(".")[1]
        fileContent = importAndParseHtmlFile(request)
        if(fileContent == "404"):
            response = "HTTP/1.1 404 Not Found \n\n The file you requested was not found on the server! \n\n"
        elif(fileType!="htm" and fileType!="html"):
            if(exists(request.lstrip("/"))):
                response = "HTTP/1.1 403 Forbidden \n\n You are not allowed to access the content of this file.\n\n"
        else:
            response = "HTTP/1.1 200 OK \n\n"+fileContent+"\n\n"
        response = bytes(response,'utf-8')
        client.sendall(response)
        client.close()

def importAndParseHtmlFile(filename):
    filename = filename.lstrip("/")
    exists(filename)
    try:
        fp = open(filename)
        response = fp.read()
        fp.close()
    except:
        return "404"
    return response

def main(port):
    sock = generateSocket(port)
    listenToRequests(sock,port)
    sock.close()

if __name__ == "__main__":
    port = int(sys.argv[1])
    main(port)
