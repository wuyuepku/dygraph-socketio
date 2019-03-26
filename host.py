from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from optparse import OptionParser
import logging, json, time
app = Flask(__name__)
socketio = SocketIO()
socketio.init_app(app=app)
logging.getLogger('werkzeug').setLevel(logging.ERROR)  # 设置不输出GET请求之类的信息，只输出error，保证控制台干净

@app.route("/")
def index():
    return app.send_static_file('index.html')

@socketio.on('connect')
def ws_connect():
    print('socketio %s connect    at: %s' % (request.remote_addr, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
@socketio.on('disconnect')
def ws_disconnect():
    print('socketio %s disconnect at: %s' % (request.remote_addr, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

def bkgtask():
    counter = 0
    while True:
        socketio.sleep(0.5)
        socketio.emit('data', counter, broadcast=True)
        counter = counter + 1
        if counter > 6:
            counter = 0
socketio.start_background_task(bkgtask)

if __name__=='__main__':
    parser = OptionParser()
    parser.add_option("--host", type="string", dest="host", help="Server Host IP", default="0.0.0.0")
    parser.add_option("--port", type="int", dest="port", help="Server Host Port", default=8080)
    options, args = parser.parse_args()
    print("\n\n##############################################")
    print("ArgosWebGui will run on port %d of '%s'" % (options.port, options.host))
    print("##############################################\n\n")
    socketio.run(app, host=options.host, port=options.port)
