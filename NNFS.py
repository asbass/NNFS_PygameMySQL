import os
import traceback
import logging
import sys
from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__, template_folder='templates')

# Cấu hình log để nhìn thấy mọi thứ trên console của Container K8s
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

def get_db():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            ssl_disabled=True
        )
    except Exception as e:
        app.logger.error(f"Database Connection Error: {str(e)}")
        raise e

def init_db():
    """Tự động kiểm tra và khởi tạo cấu trúc bảng nếu chưa tồn tại"""
    print("Checking/Initializing database tables...")
    try:
        conn = get_db()
        cursor = conn.cursor()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS scores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            player VARCHAR(255) NOT NULL,
            score INT NOT NULL
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully (Table scores is ready).")
    except Exception as e:
        # Log lỗi nếu không tạo được bảng nhưng không raise e để tránh làm sập Pod lúc init
        app.logger.error(f"Auto DB Initialization Failed: {str(e)}")

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception:
        app.logger.error(f"Home route error: {traceback.format_exc()}")
        return "Internal Server Error", 500

@app.route("/health")
def health():
    return "OK", 200

@app.route("/save-score", methods=["POST"])
def save_score():
    data = request.json
    conn = get_db()  # Mở kết nối
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO scores (player, score) VALUES (%s, %s)"
        cursor.execute(sql, (data["player"], data["score"]))
        conn.commit()
    finally:
        cursor.close()
        conn.close()  # Đóng kết nối để tránh lỗi kết nối bị treo
    return jsonify({"message": "Score Saved"})

@app.route("/leaderboard")
def leaderboard():
    conn = get_db()  # Mở kết nối
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT player, score FROM scores ORDER BY score DESC LIMIT 10")
        results = cursor.fetchall()
        leaderboard_data = [{"player": row[0], "score": row[1]} for row in results]
    finally:
        cursor.close()
        conn.close()  # Đóng kết nối
    return jsonify(leaderboard_data)

if __name__ == "__main__":
    # Tự động tạo bảng trước khi Flask Server lắng nghe request
    init_db()
    app.run(host='0.0.0.0', port=5000)
