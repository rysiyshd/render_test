import os, json, random
from flask_cors import CORS, cross_origin
from flask import Flask,jsonify,request, session,render_template,Response
from flask_socketio import SocketIO, emit, join_room, \
    leave_room, close_room, rooms, disconnect, ConnectionRefusedError

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY = "secret"
    ,JSON_AS_ASCII = False
)
socketIo = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app, responses={r"/*": {"origins": "*"}})



@app.route("/")
#@login_required
def main():
    print("main")
    #display_name = account_name(session.get("username"))
    return render_template("index.html")

@app.route('/chat/<string:room_id>')
def chat(room_id):    
    if not room_id:
        room_id = random.randrange(10**10,10**11)
        
    return render_template('meeting.html',room=room_id)

@socketIo.on('connect')
def handle_connect(data):
    print("connect",data)
    socketIo.emit('client_echo',{'msg': 'server connected!'})
    #join_room("room_1")
    
@socketIo.on('disconnect')
def disconnect():
    print("disconnect...")
    
@socketIo.on('join')
def join(data):
    print("join")
    join_room(str(data["room"]))
    socketIo.emit('join',{'msg': 'room joined!'})
    
@socketIo.on('leave')
def leave(data):
    print("leave")
    try:
        leave_room(str(data["room"]))
        socketIo.emit('leave',{'msg': 'room leaved!'})
    except:
        pass
    


# 送信ボタン押下時に実行
@socketIo.on('send_message')
def handle_message(data):
    print("handl",data)
    
    #print(data['message'])
    response_message = data['message']
    # クライアントに対してイベントを送る
    socketIo.emit('receive_message', {'message': response_message},to=data['room'])
    print('put_data')
    socketIo.emit('put_data', {'message': response_message},to=data['room'])
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5432, threaded=True)