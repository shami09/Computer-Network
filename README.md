# Computer-Networking
#Tanmeet Butani
#Net id: tsb3500
#Student ID: 3460267

#Shamika Likhite
#Net id: SLA7577
#Student Id: 3402793

This project aims with developing a web server based on https://canvas.northwestern.edu/courses/175149/files/14446240?wrap=1
It creates a simple web client and a web server using Unix socket programming and the HTTP protocol (HTTP 1.0).

Part 1: It is a simple command-line HTTP client implemented using the BSD socket interface. It runs a Unix curl command and uses python’s socket package. Only HTTP get method is supported for this program. It takes only an HTTP web address to fetch and print the body of the HTML file rfc2616.html.
The code for this part is http_client.py
Here is the code: https://github.com/tanmeet1/CS340-Northwestern/blob/main/http_client.py

Part 2: The code for this part deal with making a web server (HTTP server) that handles one client at a time.
The code for this part is http_server1.py
Here is the link to the code: https://github.com/tanmeet1/CS340Northwestern/blob/main/http_server1.py

Part 3: The server in the previous part can handle one connection at a time. The server in this part can handle multiple connections at a time.
This server avoids two main problems:
•	Waiting for connection to be established
•	Waiting on reads after connections have been established
The code for this part is http_server2.py

References: 
https://pymotw.com/3/select/
https://beej.us/guide/bgnet/html/#close-and-shutdownget-outta-my-face

Part 4: Dynamic Server
Here the server (http_server3.py) implements a JSON-based API for multiplication.
It takes contents in the form of JSON and returns the multiplied value by connecting to http_server3.
The code for this part is http_server3.py

PORT:8080 (Port on which the server runs)
http_client.py is the web client code for the project to which the server connects.
