from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from flask_socketio import emit, join_room
from backend import socketio
from backend.models import db, Act, Tag, ActTag
import os
import google.generativeai as genai
import re

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

chat_bp = Blueprint(
    "chat_bp", __name__, template_folder="templates", static_folder="static"
)

@chat_bp.route("/")
@login_required
def chat():
    return render_template("core/home.html")


@chat_bp.route("/ask", methods=["POST"])
def ask_ai():
    data = request.get_json()
    user_message = data.get('question')

    if not user_message:
        return jsonify({"error": "Question not provided"}), 400

    tags = get_all_tag_names()
    response = get_response(user_message, tags)

    if response:
        return jsonify({"answer": response})
    else:
        return jsonify({"error": "Failed to generate a response"}), 500


# WebSocket route for chat messages
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'sender': 'system', 'message': f'Cześć! W czym mogę Ci pomóc?'}, to=room)


@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    message = data['message']

    message_cleaned = clean_message(message)

    emit('message', {'sender': 'user', 'message': message}, to=room)

    tags = get_all_tag_names()
    print(tags)

    response = get_response(message_cleaned, tags)
    if response:
        bot_message = response
    else:
        bot_message = "Error while receiving response from LLM."

    emit('message', {'sender': 'bot', 'message': bot_message}, to=room)

def clean_message(message):
    message = re.sub(r'[^\w\s]', '', message)  # This removes all non-alphanumeric characters
    message = message.lower()
    return message



def get_response(message, tags):
    genai.configure(api_key=GEMINI_API_KEY)

    try:
        words = message.lower().split()

        valid_tags = [word for word in words if word in tags]
        valid_tags = filter_tags_by_act_count(valid_tags)

        if valid_tags:
            acts = get_acts_for_tags(valid_tags)
            acts_info = "\n".join([f"Tekst aktu prawnego: {act.text_payload}" for act in acts])
            ai_response = generate_ai_response(message, acts_info)
            return ai_response
        else:
            return "Na podstawie danych które posiadam nie jestem w stanie udzielić odpowiedzi. Spróbuj doprecyzować lub zmienić pytanie"

    except Exception as e:
        print(f"Error when calling a model: {e}")
        return "An error occurred while processing a message."


def generate_ai_response(user_message, acts_info):
    query = f"Użytkownik zadał pytanie: {user_message}\n\nOto powiązane akty prawne:\n{acts_info}\n\nNa podstawie tych aktów prawnych odpowiedz na pytanie użytkownika."

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query)
        if response.text:
            return response.text
        else:
            return "Nie udało się uzyskać odpowiedzi od modelu."
    except Exception as e:
        print(f"Error when generating a response from the model: {e}")
        return "An error occurred while generating the response."


def filter_tags_by_act_count(tags):
    filtered_tags = []

    for tag in tags:
        act_count = db.session.query(ActTag).join(Tag).filter(Tag.name == tag).count()

        # If there are 100 or fewer acts, keep the tag
        if act_count <= 100:
            filtered_tags.append(tag)

    return filtered_tags


def get_acts_for_tags(tags):
    acts = db.session.query(Act).join(ActTag).join(Tag).filter(Tag.name.in_(tags)).all()
    return acts


def get_all_tag_names():
    tags = db.session.query(Tag.name).all()
    return [tag.name.lower() for tag in tags]
