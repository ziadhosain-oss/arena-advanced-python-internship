import threading
from main import app as bot_app
from app import app as flask_app

def run_bot():
    bot_app.run_polling()

def run_flask():
    flask_app.run(port=5000)

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    flask_thread = threading.Thread(target=run_flask)
    bot_thread.start()
    flask_thread.start()
    bot_thread.join()
    flask_thread.join()