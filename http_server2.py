import select
import socket
import sys
import queue
from os.path import exists

inputList = []
outputList = []
responseQueue = {}

def generateSocket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.bind(("",port))
    sock.settimeout(5)
    inputList.append(sock)
    return sock

def initiateSocketForListening(sock,port):
    print('Listening for multiple connections on port ' + str(port) ,file=sys.stderr)
    sock.listen(5)
    while inputList:
        print('Waiting for the next event', file=sys.stderr)
        readInputList, writeOutputList, exceptionList = select.select(inputList,outputList,inputList)
        print(readInputList)
        # print(exceptionList)
        print(writeOutputList)
        for inputIterator in readInputList:
            if inputIterator is sock:
                print("checking if server is waiting for a connection")
                connection, client_address = inputIterator.accept()
                print('---connection from', client_address,file=sys.stderr)
                connection.setblocking(0)
                inputList.append(connection)
                responseQueue[connection] = queue.Queue()
            else:
                request = inputIterator.recv(1024)
                if request:
                    print('---received {!r} from {}'.format(request, inputIterator.getpeername()), file=sys.stderr,)
                    responseQueue[inputIterator].put(request)
                    if inputIterator not in outputList:
                        outputList.append(inputIterator)
                else:
                    print('---closing', client_address,file=sys.stderr)
                    if inputIterator in outputList:
                        outputList.remove(inputIterator)
                    inputList.remove(inputIterator)
                    del responseQueue[inputIterator]
                    inputIterator.close()
        for outputIterator in writeOutputList:
            try:
                nextMessage = responseQueue[outputIterator].get_nowait()
            except queue.Empty:
                print('  ', outputIterator.getpeername(), 'queue empty',file=sys.stderr)
                outputList.remove(outputIterator)
            else:
                nextMessage = nextMessage.decode().split("\n")[0].split(" ")[1]
                try:
                    fileType = nextMessage.split(".")[1]
                except Exception:
                    fileType = "htm"
                else:
                    fileContent = importAndParseHtmlFile(nextMessage)
                    if(fileContent == "404"):
                        nextMessage = "HTTP/1.1 404 Not Found\n\nThe file you requested was not found on the server!\n\n"
                    elif(fileType!="htm" and fileType!="html"):
                        if(exists(nextMessage.lstrip("/"))):
                            nextMessage = "HTTP/1.1 403 Forbidden\n\nYou are not allowed to access the content of this file.\n\n"
                    else:
                        nextMessage = "HTTP/1.1 200 OK \n\n"+fileContent+"\n\n"
                    nextMessage = bytes(nextMessage,'utf-8')
                    print('---sending {!r} to {}'.format(nextMessage,outputIterator.getpeername()),file=sys.stderr)
                    while True:
                        sentLength = outputIterator.send(nextMessage)
                        nextMessage = nextMessage[sentLength:]
                        if(sentLength == len(nextMessage)):
                            break
                    outputIterator.shutdown(1)
        for exceptionIterator in exceptionList:
            print('exception condition on', exceptionIterator.getpeername(),file=sys.stderr)
            inputList.remove(exceptionIterator)
            if exceptionIterator in outputList:
                outputList.remove(exceptionIterator)
            exceptionIterator.close()
            del responseQueue[exceptionIterator]

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
    initiateSocketForListening(sock,port)

if __name__ == "__main__":
    port = int(sys.argv[1])
    main(port)