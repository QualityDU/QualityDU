document.addEventListener("DOMContentLoaded", function () {
    const socket = io.connect(window.location.origin);
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    socket.on('connect', () => {
        console.log('Połączono z SocketIO!');
        socket.emit('join', { room: 'general' });
    });

    socket.on('message', (data) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(data.sender === 'user' ? 'user-message' : 'bot-message');
        messageDiv.textContent = data.message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    sendButton.addEventListener('click', function () {
        const message = messageInput.value.trim();
        if (message === "") return;

        socket.emit('send_message', { room: 'general', message });
        messageInput.value = ""; 
    });

    // Przenoszony 'keypress'
    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendButton.click();
        }
    });
});
