import socket
import sys
import json

def generateSocket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("",port))
    except Exception:
        print(Exception, sys.stderr,)
        sys.exit(-1)
    return sock

def listenToRequests(sock,port):
    #Part of this code is taken from https://pymotw.com/3/select/ and https://beej.us/guide/bgnet/html/#close-and-shutdownget-outta-my-face
    sock.listen(1)
    print("Listening for all IP addresses on port " +str(port))
    while True:
        client,client_addr = sock.accept()
        request = client.recv(2048).decode().split("\n")[0].split("?")
        print(request)
        if(request[0].split(" ")[1] != "/product"):
            response = "HTTP/1.1 404 Not Found \n\n The resource you requested was not found on the server!\n\n"
            client.sendall(bytes(response,'utf-8'))
            client.close()
            continue
        else:
            responseProductJson = {"operation":"",
                                    "operands":[],
                                    "result": 0 }
            operandList = request[1].split(" ")[0].split("&")
            product=1
            print(operandList)
            for operand in operandList:
                try:
                    number = float(operand.split("=")[1])
                    product *= number
                except Exception:
                    # print("testing")
                    response = "HTTP/1.1 400 Bad Request \n\n Your input probably wasn't a number!\n\n"
                    client.sendall(bytes(response,'utf-8'))
                    client.close()
                    break
                else:
                    responseProductJson['operands'].append(float(operand.split("=")[1]))
                    responseProductJson['operation'] = request[0].split(" ")[1].lstrip("/")
                    responseProductJson['result'] = product
                    finalResponseJson = json.dumps(responseProductJson)
                    response = "HTTP/1.1 200 OK \nContent-Type: application/json \n\n"+finalResponseJson+"\n\n"
                    response = bytes(response,'utf-8')
        client.sendall(response)
        client.shutdown(1)

def main(port):
    sock = generateSocket(port)
    listenToRequests(sock,port)

if __name__ == "__main__":
    port = int(sys.argv[1])
    main(port)