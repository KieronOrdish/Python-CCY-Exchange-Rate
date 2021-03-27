import socket 
from threading import Thread 
from bs4 import BeautifulSoup
import requests

def send_string( conn, string: str ):
    conn.sendall(( string + '\n' ).encode())

def get_rate( fromCcy, toCcy ):
    # TODO Fetch exchange rate
    url = f"https://uk.finance.yahoo.com/quote/{ fromCcy }{ toCcy }%3DX?p={ fromCcy }{ toCcy }%3DX"
    data = requests.get( url )
    soup = BeautifulSoup( data.text, "html.parser" )
    return soup.find( "span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" ).get_text()

class ClientThread( Thread ): 
    def __init__( self, ip, port, conn ): 
        Thread.__init__( self ) 
        self.ip = ip 
        self.port = port 
        self.conn = conn
        send_string( self.conn, "To exit type exit")

    def run( self ): 
        try:
            while True : 
                try:
                    data = self.conn.recv( 1028 ).decode()
                    data = data.rstrip()
                    if data == 'exit':
                        # close the connection
                        try:
                            self.conn.close()
                        except:
                            pass
                        return
                    fromCcy, toCcy = data.split( ':' )
                    rate = get_rate( fromCcy, toCcy )
                    send_string( self.conn, rate )
                except:
                    send_string( self.conn, "Bad Request please put in form of USD:EUR" )
        except socket.error:
            #  if there is an error close the connection
            try:
                self.conn.close()
            except:
                pass
            return

# Multithreaded Python server
HOST = 'localhost' 
PORT = 8080
server = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) 
server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 ) 
server.bind(( HOST, PORT )) 
server.listen( 4 ) 
print( "Multithreaded Python server online" )

try: 
    while True: 
        ( conn, ( ip, port )) = server.accept() 
        newthread = ClientThread( ip, port, conn ) 
        newthread.daemon = True
        newthread.start()
except:
    server.shutdown
    server.close()
    print( "server ended" )
