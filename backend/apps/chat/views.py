from flask import Blueprint, render_template
from flask_login import login_required
from flask_socketio import emit, join_room, leave_room
from backend import socketio
from backend.models import db, Act
import os
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# TODO: dodac endpoint do wysylania wiadomosci do bota

chat_bp = Blueprint(
    "chat_bp", __name__, template_folder="templates", static_folder="static"
)


@chat_bp.route("/")
@login_required
def chat():
    return render_template("core/home.html")


@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)

    emit('message', {'sender': 'system', 'message': f'Cześć! W czym mogę Ci pomóc?'}, to=room)


@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    message = data['message']

    emit('message', {'sender': 'user', 'message': message}, to=room)

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    acts_string = get_all_acts_as_string()
    response = model.generate_content('W kontekście' + acts_string + 'odpowiedz na pytanie' + message + '. Odpowiedz '
                                                                                                        'udzielaj w '
                                                                                                        'języku '
                                                                                                        'polskim')

    if response and hasattr(response, 'text'):
        bot_message = response.text
    else:
        bot_message = "Error while receiving response from LLM."

    emit('message', {'sender': 'bot', 'message': bot_message}, to=room)


def get_all_acts_as_string():
    acts = db.session.query(Act).all()

    acts_string = "\n".join([
        f"Act ID: {act.act_id}, DU Code: {act.du_code}, Year: {act.year}, Journal No: {act.journal_no}, Text: {act.text_payload}"
        for act in acts])
    return acts_string
