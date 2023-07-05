import argparse
import socket
import aiohttp.web
import socketio
import webview
import constants

#! Parse CLI arguments
parser = argparse.ArgumentParser(description="PyWebview app template")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument("--dev", action="store_true", help="Enable development mode")
args = parser.parse_args()

#! Get URL for webview window
def get_url(dev: bool, debug: bool, socketio_port: int | str) -> str:
    if dev:
        url = f"http://localhost:{constants.DEV_SERVER_PORT}/" 
    else:
        url = f"./res/dist/index.html"
    
    url += f"?dev={'true' if dev else 'false'}"
    url += f"&debug={'true' if debug else 'false'}"
    url += f"&socketio_port={socketio_port}"
    
    return url

#! Get an available port for SocketIO
def get_free_port() -> int:
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

#! SocketIO server object
sio_port = get_free_port()
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = aiohttp.web.Application()
sio.attach(app)

#! Webview window object
window = webview.create_window('Window', get_url(args.dev, args.debug, sio_port))

#! SocketIO Events
@sio.event
def connect(sid, environ):
    print("connect ", sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

#! SocketIO message event
@sio.on("message")
def on_message(sid, event, data):
    print(f'Message from {sid}: ', data)

#! Start function
def main():
    aiohttp.web.run_app(app, port=sio_port)

if __name__ == '__main__':
    webview.start(debug=True, http_server=True, func=main)