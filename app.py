from flask import Flask, render_template, request, jsonify
from rule_based_chatbot import RuleBasedChatbot
import webbrowser
import threading
import time

app = Flask(__name__)
bot = RuleBasedChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    bot_response = bot.get_response(user_message)
    return jsonify({'response': bot_response})

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:3001')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True, port=3001, use_reloader=False)