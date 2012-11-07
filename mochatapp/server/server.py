import os

import eventlet
from eventlet import wsgi
from eventlet import websocket

PORT = 7000

participants = set()

@websocket.WebSocketWSGI
def handle(ws):
    participants.add(ws)
    try:
        while True:
            m = ws.wait()
            if m is None:
                break
            for p in participants:
                p.send(m)
    finally:
        participants.remove(ws)
                  
def dispatch(environ, start_response):
    return handle(environ, start_response)
        
if __name__ == "__main__":
    # run an example app from the command line            
    listener = eventlet.listen(('127.0.0.1', PORT))
    print "\nVisit http://localhost:7000/ in your websocket-capable browser.\n"
    wsgi.server(listener, dispatch)