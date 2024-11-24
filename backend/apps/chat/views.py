from flask import Blueprint
from flask_login import login_required
from flask_socketio import emit, join_room, leave_room
from backend import socketio

chat_bp = Blueprint(
    "chat_bp", __name__, template_folder="templates", static_folder="static"
)


@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    
    emit('message', {'sender': 'system', 'message': f'Użytkownik dołączył do pokoju {room}.'}, to=room)
    

@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    message = data['message']

    emit('message', {'sender': 'user', 'message': message}, to=room)
    emit('message', {'sender': 'bot', 'message': f'Odpowiedź na: {message}'}, to=room)
    
