import socket
import sys

def makeSocket():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setblocking(True)
    return sock

def sendRequest(socket,host,resource,port):
    headers = "GET "+resource+" HTTP/1.1\r\nHost: "+host+"\r\nAccept: */*\r\n\r\n"
    socket.connect((host,port))
    socket.sendall(headers.encode())
    return readResopnse(socket)

def readResopnse(socket):
    fileError = open("errors.log","w")
    buffer_size = 2048
    response = b''
    while True:
        buffer = socket.recv(buffer_size)
        print(buffer, file = fileError,)
        response += buffer
        if len(buffer) < buffer_size and (buffer.decode().find("</html>")!=-1 or buffer.decode().find("</HTML>")!=-1):
            break
    fileError.close()
    return response.decode("utf-8","ignore")

def getHTTPResponse(response):
    return processStatusCode(response.split(" ")[1],response)

def findLocationHeader(response):
    if(response):
        iter = response.split("\n\n")[0].count("\n")
        iter = int(iter/2)
    headers = {}
    for i in range(1,iter):
        headers[response.split("\n")[i].split(":")[0].strip()] = response.split("\n")[i].split(":")[1:]
    if("Location" in headers):
        headers['Location'] = (headers['Location'][0]+":"+headers['Location'][1]).strip()
        return headers,headers['Location']
    return headers

def processStatusCode(statusCode,response):
    host = "testHost"
    headers = findLocationHeader(response)
    if(statusCode == '200'):
        1
    elif(statusCode == '301'):
        host = findLocationHeader(response)
        print("Redirected to",None,sys.stderr)
        host = processHost(host[1])
        # print(host, sys.stderr,)
    elif(statusCode == '302'):
        host = findLocationHeader(response)
        print("Redirected to",None,sys.stderr)
        host = processHost(host[1])
        # print(host, sys.stderr,)
    if(int(statusCode)>=400):
        1
    return statusCode,host,headers

def printToStdout(response):
    print(response.split("\r\n\r\n")[1].split("<body")[1].split("</body>")[0])
def main(host):
    resource = host[1]
    port = host[2]
    host = host[0]
    statusCode=0
    i=0
    while((int(statusCode)<400 and statusCode != '200') or i>10):
        socket = makeSocket()
        response = sendRequest(socket,host,resource,port)
        statusCode,host,headers = getHTTPResponse(response)
        resource = host[1]
        host = host[0]
        i+=1
        socket.close()
    # print(headers['Content-Type'][0].strip())
    if("Content-Type" in headers and headers['Content-Type'][0].strip().split(";")[0] == "text/html"):
        if("<body " in response.split("\r\n\r\n")[1]): 
            printToStdout(response)
            return(sys.exit(0))
        elif("<body>" in response.split("\r\n\r\n")[1]):
            printToStdout(response)
            return(sys.exit(0))
    elif("Content-Type" not in headers):
        try:
            printToStdout(response)
            return(sys.exit(0))
        except:
            return(sys.exit(-1))
    return(sys.exit(-1))

def processHost(hostaddr):
    if("https://" in hostaddr):
        print("https url received, exiting", sys.stderr,)
        sys.exit(-1)
    port = 80
    if(":" in hostaddr.split("http://")[0]):
        hostaddr = hostaddr.split(":")[0]
        port = hostaddr.split(":")[1]
    hostaddr = hostaddr.lstrip("http://")
    host = hostaddr.split("/")[0]
    if(len(hostaddr.split("/"))>1 and hostaddr.split("/")[1]!=""):
        resource = "/"+hostaddr.split("/")[1]
    else:
        resource = "/"
    return host,resource.rstrip(),port

if __name__ == "__main__":
    host = processHost(sys.argv[1])
    main(host)