import aiohttp.web
import socketio
import webview

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = aiohttp.web.Application()
sio.attach(app)

window = webview.create_window('Window', 'http://localhost:5173')

@sio.event
def connect(sid, environ):
    print("connect ", sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

def main():
    aiohttp.web.run_app(app, port=8080)

if __name__ == '__main__':
    webview.start(debug=True, http_server=True, func=main)