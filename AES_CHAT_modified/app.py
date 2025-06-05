from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from collections import defaultdict


app = Flask(__name__)
socketio = SocketIO(app)

# Store username -> sid mapping
users = {}

# Store sid -> username mapping
sid_to_username = {}

# Chat history per room (room named by "user1:user2" sorted)
chat_history = defaultdict(list)

def get_room(user1, user2):
    return ":".join(sorted([user1, user2]))

@app.route("/")
def index():
    return render_template("temp_index.html")

@app.route('/chat')
def chat():
    # Render the chat page (the chat system HTML)
    return render_template('chat.html')

if __name__ == "__main__":
    app.run(debug=True)

@socketio.on("login")
def on_login(data):
    username = data.get("username", "").strip()
    sid = request.sid
    users[username] = sid
    sid_to_username[sid] = username
    print(f"{username} logged in with sid {sid}")
    emit("users_update", list(users.keys()), broadcast=True)
    print("Current users:", users)

@socketio.on("send_message")
def handle_send_message(data):
    sender_sid = request.sid
    sender = sid_to_username.get(sender_sid)
    recipient = data.get("to")
    encrypted_data = data.get("data")
    if not sender or not recipient.strip() or not encrypted_data.strip():
        return

    room = get_room(sender, recipient)
    # Save message in room history
    chat_history[room].append({
        "from": sender,
        "to": recipient,
        "data": encrypted_data
    })

    # Send message only to sender and recipient if connected
    recipient_sid = users.get(recipient)
    if recipient_sid:
        emit("receive_message", {
            "from": sender,
            "to": recipient,
            "data": encrypted_data
        }, room=recipient_sid)

    # Also send to sender (so sender can see their sent message)
    emit("receive_message", {
        "from": sender,
        "to": recipient,
        "data": encrypted_data
    }, room=sender_sid)

@socketio.on("request_history")
def handle_request_history(data):
    user = sid_to_username.get(request.sid)
    chat_with = data.get("chatWith")
    if not user or not chat_with:
        return
    room = get_room(user, chat_with)
    for msg in chat_history[room]:
        # Send only messages that belong to this room (should be all)
        emit("receive_message", msg)

@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    username = sid_to_username.get(sid)
    if username:
        users.pop(username, None)
        sid_to_username.pop(sid, None)
        print(f"{username} disconnected")
        emit("users_update", list(users.keys()), broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=3000, debug=False, use_reloader=False)
