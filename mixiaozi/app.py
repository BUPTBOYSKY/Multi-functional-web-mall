from flask import Flask, send_from_directory, request, jsonify
import pymysql
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# 数据库连接信息
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', '121.41.116.214'),
        user=os.getenv('DB_USER', 'sijiatong'),
        passwd=os.getenv('DB_PASSWORD', 'SAU6nygP6Jef7wFr'),
        port=int(os.getenv('DB_PORT', 3306)),
        db=os.getenv('DB_NAME', 'mixiaozi'),
        charset='utf8'
    )

# 初始化数据库
def init_database():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
            """
            cursor.execute(sql)
        conn.commit()
        print("数据库初始化完成")

        with conn.cursor() as cursor:
            sql = """
             CREATE TABLE IF NOT EXISTS images (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                 image_name VARCHAR(255),
                 image_data LONGBLOB
             )
             """
            cursor.execute(sql)
        conn.commit()
        print("数据库初始化完成")
    except Exception as e:
        print(f"数据库初始化失败：{str(e)}")
    finally:
        conn.close()

init_database()

# Serve all HTML files from the 'static' directory
@app.route('/')
@app.route('/<path:path>')
def serve_static(path='登录.html'):
    return send_from_directory(app.static_folder, path)

# Register user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求数据为空'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '用户名或密码不能为空'}), 400

    conn = get_db_connection()
    try:
        hashed_password = generate_password_hash(password)
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, hashed_password))
        conn.commit()
        return jsonify({'message': '注册成功'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# Login user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求数据为空'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '用户名或密码不能为空'}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT password FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result and check_password_hash(result[0], password):
                return jsonify({'message': '登录成功'}), 200
            else:
                return jsonify({'error': '用户名或密码错误'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# Save image to database
@app.route('/save_image_to_db', methods=['POST'])
def save_image_to_db():
    conn = get_db_connection()
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'})

        file = request.files['image']
        image_name = file.filename

        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'})

        if file:
            image_data = file.read()

            with conn.cursor() as cursor:
                sql = "INSERT INTO images (image_name, image_data) VALUES (%s, %s)"
                cursor.execute(sql, (image_name, image_data))
            conn.commit()

            return jsonify({'success': True})
    except Exception as e:
        print(f"Error saving image to DB: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
