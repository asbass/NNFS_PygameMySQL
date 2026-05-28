from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Config
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"), # Lấy từ biến môi trường, mặc định là localhost
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASS", ""),
    database="gameboard"
)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player VARCHAR(50),
    score INT
)
""")

db.commit()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/save-score", methods=["POST"])
def save_score():
    data = request.json

    player = data["player"]
    score = data["score"]

    sql = "INSERT INTO scores (player, score) VALUES (%s, %s)"
    val = (player, score)

    cursor.execute(sql, val)
    db.commit()

    return jsonify({"message": "Score Saved"})


@app.route("/leaderboard")
def leaderboard():

    cursor.execute("""
    SELECT player, score
    FROM scores
    ORDER BY score DESC
    LIMIT 10
    """)

    results = cursor.fetchall()

    leaderboard_data = []

    for row in results:
        leaderboard_data.append({
            "player": row[0],
            "score": row[1]
        })

    return jsonify(leaderboard_data)


if __name__ == "__main__":
    app.run(debug=True)
