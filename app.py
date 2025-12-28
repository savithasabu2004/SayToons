from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# ✅ Add your OpenAI API Key here
client = OpenAI(api_key="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")


# 🟢 Health Check Route
@app.route("/")
def home():
    # Serve the welcome HTML page when visiting the site root
    try:
        return send_file('welcome.html')
    except Exception:
        return "SayToons AI Backend is Running ✅"


# 🟢 Get Levels (Already works with your frontend)
@app.route("/get-levels", methods=["GET"])
def get_levels():
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT level_no, level_name FROM levels")
        levels = [{"level_no": r[0], "level_name": r[1]} for r in cursor.fetchall()]
        conn.close()
        return jsonify(levels)
    except Exception as e:
        print("❌ DB error:", e)
        return jsonify([])


# ✅ FUNCTION 1 — Get image from database if exists
def get_saved_image(phrase):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT image_url FROM tasks WHERE phrase=?", (phrase,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


# ✅ FUNCTION 2 — Save new image into database
def save_image(phrase, level, image_url):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO tasks (phrase, level, image_url) VALUES (?, ?, ?)",
        (phrase, level, image_url)
    )
    conn.commit()
    conn.close()


# 🟢 📸 MAIN ROUTE — Convert phrase → AI cartoon image
@app.route("/get-image-by-phrase", methods=["POST"])
def get_image():
    data = request.get_json()
    phrase = data.get("phrase", "").lower()
    level = data.get("level", "").lower()

    if not phrase:
        return jsonify({"error": "No phrase provided"}), 400

    # ✅ Check cache first
    saved_image = get_saved_image(phrase)
    if saved_image:
        return jsonify({"phrase": phrase, "image_url": saved_image})

    # ❌ Not found → generate using AI
    try:
        prompt = f"A colorful, cute cartoon illustration for children showing {phrase} during {level or 'daily life'}."
        result = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024"
        )
        image_url = result.data[0].url

        # ✅ Save for future use
        save_image(phrase, level, image_url)

        return jsonify({"phrase": phrase, "image_url": image_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
