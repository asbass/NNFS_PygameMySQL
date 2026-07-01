import os
from flask import Flask, render_template, request, jsonify
import mysql.connector
import sys
app = Flask(__name__)

# Hàm tạo kết nối Database (đảm bảo mỗi lần gọi là một kết nối tươi mới)
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=True
    )

# Hàm khởi tạo bảng (chạy 1 lần duy nhất khi ứng dụng khởi động)
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player VARCHAR(50),
        score INT
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Gọi hàm khởi tạo bảng
init_db()

@app.route("/health")
def health():
    return "OK", 200

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/save-score", methods=["POST"])
def save_score():
    data = request.json
    conn = get_db() # Mở kết nối
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO scores (player, score) VALUES (%s, %s)"
        cursor.execute(sql, (data["player"], data["score"]))
        conn.commit()
    finally:
        cursor.close()
        conn.close() # Đóng kết nối để tránh lỗi kết nối bị treo
    return jsonify({"message": "Score Saved"})

@app.route("/leaderboard")
def leaderboard():
    conn = get_db() # Mở kết nối
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT player, score FROM scores ORDER BY score DESC LIMIT 10")
        results = cursor.fetchall()
        leaderboard_data = [{"player": row[0], "score": row[1]} for row in results]
    finally:
        cursor.close()
        conn.close() # Đóng kết nối
    return jsonify(leaderboard_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
