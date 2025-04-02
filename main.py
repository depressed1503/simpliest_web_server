from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('text_storage.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS texts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  content TEXT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/store_text', methods=['POST'])
def store_text():
    if request.is_json:
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Empty JSON payload'}), 400
                
            text = data.get('text')
            if not text:
                return jsonify({'error': 'Missing "text" field in JSON'}), 400
        except Exception as e:
            return jsonify({'error': 'Invalid JSON format', 'details': str(e)}), 400
    else:
        # Handle raw text
        text = request.data.decode('utf-8').strip()
        if not text:
            return jsonify({'error': 'No text content provided'}), 400

    # Store in database
    try:
        conn = sqlite3.connect('text_storage.db')
        c = conn.cursor()
        c.execute("INSERT INTO texts (content) VALUES (?)", (text,))
        conn.commit()
        return jsonify({
            'message': 'Text stored successfully',
            'text': text,
            'status': 'ok'
        }), 201
    except Exception as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)